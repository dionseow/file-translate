import os
from typing import Callable
import os
import fitz
from schemas.file import Processor

DEFAULT_FONT = "Times-Roman"
OVERLAP_OFFSET = 5

class PDFProcessor(Processor):
    def extract_text(self, file_path: str | os.PathLike) -> str:
        doc = fitz.open(file_path)

        extracted_text = ""

        for _, page in enumerate(doc):
            blocks = page.get_text("dict", sort=False)["blocks"]

            for block in blocks:
                if block.get("lines", None):
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if not text:
                                continue
                            extracted_text = extracted_text + "\n" + text
        
        return extracted_text


    def translate_in_place(self, file_path: str | os.PathLike, new_file_path: str | os.PathLike, translator: Callable[[str], str]) -> None:
        pass
    #     doc = fitz.open(file_path)

    #     for _, page in enumerate(doc):
    #         blocks = page.get_text("dict", sort=False)["blocks"]
    #         # fonts = doc.get_page_fonts(page_no) # unused - refer to _get_font_name desc
    #         spans = []

    #         for block in blocks:
    #             if block.get("lines", None):
    #                 for line in block["lines"]:
    #                     for span in line["spans"]:
    #                         text = span["text"].strip()
    #                         if not text:
    #                             continue
    #                         spans.append(span)
            
    #         for span in spans:
    #             bbox = span["bbox"]
    #             page.add_redact_annot(bbox)
    #             page.apply_redactions()
            
    #         merged_spans = self._merge_spans(spans)

    #         for span in merged_spans:
    #             text = span["text"]
    #             sentences = [sent.text for sent in self.spacy_model(text).sents]
    #             translated_sentences = [translator(sent) for sent in sentences]
    #             translated_text = (" ").join(translated_sentences)
    #             font_size = span["size"]

    #             inserted = page.insert_textbox(span['bbox'],
    #                                             translated_text,
    #                                             fontname=DEFAULT_FONT,
    #                                             fontsize=font_size,
    #                                             )
    #             if inserted < 0:
    #                 while inserted < 0:
    #                     font_size -= 2
    #                     inserted = page.insert_textbox(span['bbox'],
    #                                                     translated_text,
    #                                                     fontname=DEFAULT_FONT,
    #                                                     fontsize=font_size,
    #                                                     )

    #     doc.save(new_file_path, garbage=4, deflate=True, clean=True)
    
    # def _merge_spans(self, spans, delta_x=0.1, delta_y=0.1):
    #     def is_in_bbox(point, bbox):
    #         """
    #         Arguments:
    #             point {list} -- list of float values (x,y)
    #             bbox {list} -- bounding box of float_values [xmin, ymin, xmax, ymax]
    #         Returns:
    #             {boolean} -- true if the point is inside the bbox
    #         """
    #         return point[0] >= bbox[0] and point[0] <= bbox[2] and point[1] >= bbox[1] and point[1] <= bbox[3]

    #     def intersect(bbox1, bbox2):
    #         """
    #         Arguments:
    #             bbox {list} -- bounding box of float_values [xmin, ymin, xmax, ymax]
    #             bbox_ {list} -- bounding box of float_values [xmin, ymin, xmax, ymax]
    #         Returns:
    #             {boolean} -- true if the bboxes intersect
    #         """
    #         for i in range(int(len(bbox1) / 2)):
    #             for j in range(int(len(bbox1) /
    #                 # Check if one of the corner of bbox inside bbox_
    #                 if is_in_bbox([bbox1[2 * i], bbox1[2 * j + 1]], bbox2):
    #                     return True
    #         return False

    #     merged_spans = []
    #     for span in spans:
    #         merged = False
    #         bbox_1 = span['bbox']
    #         for i, span_2 in enumerate(merged_spans):
    #             bbox_2 = span_2['bbox']

    #             bbox_1_margin = [
    #                 bbox_1[0] - (bbox_1[2] - bbox_1[0]) * delta_x, bbox_1[1] - (bbox_1[3] - bbox_1[1]) * delta_y,
    #                 bbox_1[2] + (bbox_1[2] - bbox_1[0]) * delta_x, bbox_1[3] + (bbox_1[3] - bbox_1[1]) * delta_y
    #             ]

    #             bbox_2_margin = [
    #                 bbox_2[0] - (bbox_2[2] - bbox_2[0]) * delta_x, bbox_2[1] - (bbox_2[3] - bbox_2[1]) * delta_y,
    #                 bbox_2[2] + (bbox_2[2] - bbox_2[0]) * delta_x, bbox_2[3] + (bbox_2[3] - bbox_2[1]) * delta_y
    #             ]

    #             # Merge bboxes if bboxes with margin has an intersection
    #             if intersect(bbox_1_margin, bbox_2_margin) or intersect(bbox_2_margin, bbox_1_margin):
    #                 tmp_bbox = (min(bbox_1[0], bbox_2[0]), min(bbox_1[1], bbox_2[1]),
    #                             max(bbox_1[2], bbox_2[2]), max(bbox_1[3], bbox_2[3]))
    #                 tmp_text = span_2["text"] + " " + span["text"]
    #                 merged_spans[i] = {"bbox": tmp_bbox, "text": tmp_text, "size": span['size']}
    #                 merged = True
    #                 break
    #         if not merged:
    #             merged_spans.append(span)
    #     return merged_spans