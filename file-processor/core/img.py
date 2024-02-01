import os
import cv2
import numpy as np

from typing import Callable
from paddleocr import PaddleOCR
from schemas.file import Processor

ocr = PaddleOCR(
    det_model_dir="/app/models/en_PP-OCRv3_det_infer",
    rec_model_dir="/app/models/en_PP-OCRv3_rec_infer",
    cls_model_dir="/app/models/ch_ppocr_mobile_v2.0_cls_infer",
    use_angle_cls=True, lang="en")


class ImageProcessor(Processor):
    def extract_text(self, file_path: str | os.PathLike) -> str:
        ocr_result = ocr.ocr(file_path, cls=True)
        result = ocr_result[0]

        extracted_text = ""

        for line in result:
            text = line[1][0]
            text = text.strip()
            if text:
                extracted_text = extracted_text + "\n" + text
        
        return extracted_text


    def translate_in_place(self, file_path: str | os.PathLike, new_file_path: str | os.PathLike, translator: Callable[[str], str]) -> None:
        pass
        # ocr_result = ocr.ocr(file_path, cls=True)
        # result = ocr_result[0]
        # image = cv2.imread(file_path)
        # font = cv2.FONT_HERSHEY_SIMPLEX

        # # Draw boxes around predicted text locations in original image
        # for line in result:
        #     box = line[0]
        #     top_left = tuple([int(i) for i in box[0]])
        #     bottom_right = tuple([int(i) for i in box[2]])
        #     image = cv2.rectangle(image, top_left, bottom_right, (0,255,0), 3)
        
        # duplicate_image = image.copy()
        # for line in result:
        #     box = line[0]
        #     text = line[1][0]
        #     x_box = [int(i[0]) for i in box]
        #     y_box = [int(i[1]) for i in box]

        #     x1 = min(x_box)
        #     x2 = max(x_box)
        #     box_width = x2 - x1

        #     y1 = min(y_box)
        #     y2 = max(y_box)
        #     box_height = y2 - y1

        #     # Blank out current text box
        #     duplicate_image[y1:y2, x1:x2] = (255, 255, 255)
        #     roi = duplicate_image[y1:y2, x1:x2]
        #     translated_text = translator(text)

        #     font_scale = 1
        #     text_color = (0, 0, 255) # Red
        #     text_thickness = 2

        #     text_size, _ = cv2.getTextSize(translated_text, font, font_scale, text_thickness)
        #     scaling_factor = min(box_width / text_size[0], box_height / text_size[1])
        #     scaled_font_scale = font_scale * scaling_factor
        #     scaled_text_size, _ = cv2.getTextSize(translated_text, font, scaled_font_scale, text_thickness)

        #     scaled_text_x = x1 + (box_width - scaled_text_size[0]) // 2
        #     scaled_text_y = y1 + (box_height + scaled_text_size[1]) // 2
        #     cv2.putText(duplicate_image, translated_text, (scaled_text_x, scaled_text_y), font, scaled_font_scale, (0, 0, 255), text_thickness)
        
        # # Put original + translated image side by side
        # result = np.concatenate((image, duplicate_image), axis=1)
        # cv2.imwrite(new_file_path, result)