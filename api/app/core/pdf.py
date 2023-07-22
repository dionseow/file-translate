import os
from typing import Callable
import os
import fitz
import math
import spacy
from app.schemas.bbox import BoundingBox, bbox_to_tuple, combine_bboxes,check_if_bbox_overlap
from app.schemas.file import FileTranslator

DEFAULT_FONT = "Times-Roman"
OVERLAP_OFFSET = 5

class PDFTranslator(FileTranslator):
    def init(self):
        self.spacy_model = spacy.load("en_core_web_sm")

    def translate_in_place(self, file_path: str | os.PathLike, new_file_path: str | os.PathLike, translator: Callable[[str], str]) -> None:
        doc = fitz.open(file_path)

        for _, page in enumerate(doc):
            blocks = page.get_text("dict", sort=False)["blocks"]
            # fonts = doc.get_page_fonts(page_no) # unused - refer to _get_font_name desc
            page_spans = []
            for block in blocks:
                if block.get("lines", None):
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if not text:
                                continue
                            page_spans.append(span)
            
            new_spans = self._combine_spans_by_text_segmentation(page_spans)
            adjusted_spans = self._adjust_spans_to_not_overlap(page_spans)

            for span in adjusted_spans:
                text = span["text"].strip()
                translated_text = translator(text)
                bbox = span["bbox"]
                font_size = span["size"]
                adjusted_font_size = self._get_adjusted_font_size(translated_text, DEFAULT_FONT, font_size, bbox)
                page.add_redact_annot(bbox)
                page.apply_redactions()
                inserted = page.insert_textbox(bbox,
                                                translated_text,
                                                fontname=DEFAULT_FONT,
                                                fontsize=adjusted_font_size,
                                                )
                if inserted < 0:
                    while True:
                        adjusted_font_size -= 1
                        inserted = page.insert_textbox(bbox,
                                                        translated_text,
                                                        fontname=DEFAULT_FONT,
                                                        fontsize=adjusted_font_size,
                                                        )
                        if inserted > 0:
                            break
        doc.save(new_file_path, garbage=4, deflate=True, clean=True)

# Unused. To dynamically replace text with the same font as the document, it would
    # require loading a .ttf file locally.
    # https://github.com/pymupdf/PyMuPDF/discussions/1532
    def _get_font_name(self, font_list, base_font):
        """
        PyMuPDF represents fonts as a shortened version (base font) and a full version
        The blocks function only returns the base font, while the insert_textbox
        function requires the full version. This function is required to resolve
        the base font to the full font string
        """
        default_font = "Times-Roman"
        for font in font_list:
            curr_base = font[3]
            font_name = font[4]
            if base_font in curr_base:
                return font_name
            else:
                return default_font
    
    def _get_adjusted_font_size(self, text: str, font_name: str, font_size: int, bbox: tuple) -> int:
        # Doesnt check for height, not sure if can be done
        rect_width = bbox[0] - bbox[1]
        text_length = fitz.get_text_length(text, fontsize=font_size, fontname=font_name)
        if text_length >= rect_width:
            while True:
                font_size -= 1
                text_length = fitz.get_text_length(text, fontsize=font_size, fontname=font_name)
                if not text_length >= rect_width:
                    break
        return font_size
    
    def _add_text_to_page(self, page: fitz.Page, bbox: tuple, text: str, font_name:str, font_size:int) -> None:
        height_deficit = page.insert_textbox(bbox,
                                             text,
                                             fontname=font_name,
                                             fontsize=font_size)
        if height_deficit < 0:
            while height_deficit < 0:
                font_size -= 1
                height_deficit = page.insert_textbox(bbox,
                                                    text,
                                                    fontname=font_name,
                                                    fontsize=font_size)
    
    def _adjust_spans_to_not_overlap(self, spans):
        for i in range(len(spans)):
            for j in range(i + 1, len(spans)):
                if check_if_bbox_overlap(spans[i]['bbox'], spans[j]['bbox']):
                    (x_min, y_min, x_max, y_max) = spans[i]['bbox']
                    box_1 = BoundingBox(x_min, y_min, x_max, y_max)
                    (x_min, y_min, x_max, y_max) = spans[j]['bbox']
                    box_2 = BoundingBox(x_min, y_min, x_max, y_max)

                    # calculate overlap dimensions
                    x_overlap = min(box_1.x_max, box_2.x_max) - max(box_1.x_min, box_2.x_min)
                    y_overlap = min(box_1.y_max, box_2.y_max) - max(box_1.y_min, box_2.y_min)

                    if x_overlap < y_overlap:
                        # Adjust horizontally
                        if box_1.x_max < box_2.x_max:
                            box_1.x_max = box_2.x_min - OVERLAP_OFFSET
                        else:
                            box_1.x_min = box_2.x_max + OVERLAP_OFFSET
                    else:
                        # Adjust vertically
                        if box_1.y_max < box_2.y_max:
                            box_1.y_max = box_2.y_min - OVERLAP_OFFSET
                        else:
                            box_1.y_min = box_2.y_max + OVERLAP_OFFSET

                    spans[i]['bbox'] = bbox_to_tuple(box_1)
                    spans[j]['bbox'] = bbox_to_tuple(box_2)
        return spans
    
    def _combine_spans_by_text_segmentation(self, spans):
        span_texts = [span["text"].strip() for span in spans]
        combined_text = (" ").join(span_text)
        doc = self.spacy_model(combined_text)
        segmented_texts = [sent.text for sent in doc.sents]

        span_to_segmented_text_mapping = {}
        for span_index, span_text in enumerate(span_texts):
            for segmented_index, segmented_text in enumerate(segmented_texts):
                if segmented_text.endswith(span_text):
                    span_to_segmented_text_mapping[span_index] = segmented_index
        
            if not span_to_segmented_text_mapping.get(len(span_texts), None):
                span_to_segmented_text_mapping[len(span_texts)] = len(segmented_texts)
            
            new_spans = []
            for span_index, segmented_index in span_to_segmented_text_mapping.items():