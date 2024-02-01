from dataclasses import dataclass, fields, is_dataclass

@dataclass
class BoundingBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float


# def is_in_bbox(point: list(float), bbox: BoundingBox) -> bool:
#     return point[0] >= bbox[0] and point[0] <= bbox[2] and point[1] >= bbox[1] and point[1] <= bbox[3]

# def intersect(bbox_1: BoundingBox, bbox_2: BoundingBox) -> bool:
#     for i in range(int(len(bbox_1) / 2)):
#         for j in range(int(len(bbox_1) / 2)):
#             # Check if one of the corner of bbox inside bbox_
#             if is_in_bbox([bbox_1[2 * i], bbox_1[2 * j + 1]], bbox_2):
#                 return True
#     return False

# def good_intersect(bbox_1: BoundingBox, bbox_2: BoundingBox) -> bool:
#     return (bbox_1[0] < bbox_2[2] and bbox_1[2] > bbox_2[0] and
#             bbox_1[1] < bbox_2[3] and bbox_1[3] > bbox_2[1])



# def bbox_to_tuple(bbox: BoundingBox) -> tuple:
#     if not is_dataclass(bbox):
#         raise ValueError("Input object is not a dataclass")
    
#     class_fields = fields(bbox)
#     values = tuple(getattr(bbox, field.name) for field in class_fields)
#     return values

# def check_if_bbox_overlap(box1: BoundingBox, box2: BoundingBox) -> bool:
#     if (box1[0] > box2[2] or box2[0] > box1[2]):
#         return False  # No intersection along the x-axis

#     if (box1[1] > box2[3] or box2[1] > box1[3]):
#         return False  # No intersection along the y-axis

#     return True  # Intersection exists

# def combine_bboxes(bboxes: list[BoundingBox]) -> BoundingBox:
#     min_x, min_y = float('inf'), float('inf')
#     max_x, max_y = float('-inf', float('-inf'))

#     for box in bboxes:
#         x1, y1 ,x2 ,y2 = box.x_min, box.y_min, box.x_max, box.y_max

#         # Update the min and max coords
#         min_x = min(min_x, x1)
#         min_y = min(min_y, y1)
#         max_x = max(max_x, x2)
#         max_y = max(max_y, y2)
    
#     return BoundingBox(min_x, min_y, max_x, max_y)