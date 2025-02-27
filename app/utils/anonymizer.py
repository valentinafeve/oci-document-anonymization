import matplotlib.patches as patches
import matplotlib.pyplot as plt
import io

def xyxy_to_xywh(x1, y1, x2, y2):
    return x1, y1, x2 - x1, y2 - y1

def xyxy_to_cxcywh(x1, y1, x2, y2):
    return (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1

def anonymize(image, words):
    fig, ax = plt.subplots()
    width, height = image.width, image.height

    ax.imshow(image)

    for word in words:
        x, y, w, h = xyxy_to_xywh(word["boundingPolygon"]["normalizedVertices"][1]["x"], word["boundingPolygon"]["normalizedVertices"][1]["y"],
                                    word["boundingPolygon"]["normalizedVertices"][3]["x"], word["boundingPolygon"]["normalizedVertices"][3]["y"])
        
        cx, cy, w, h = xyxy_to_cxcywh(word["boundingPolygon"]["normalizedVertices"][1]["x"], word["boundingPolygon"]["normalizedVertices"][1]["y"],
                                    word["boundingPolygon"]["normalizedVertices"][3]["x"], word["boundingPolygon"]["normalizedVertices"][3]["y"])
        
        rect = patches.Rectangle((x * width, y * height), w * width, h * height, linewidth=1, edgecolor='white', facecolor='white')

        ax.add_patch(rect)

    ax.set_axis_off()

    buffer = io.BytesIO()  # use buffer memory
    plt.savefig(buffer, format="png", bbox_inches='tight', pad_inches=0)
    return buffer
