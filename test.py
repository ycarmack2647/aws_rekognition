import boto3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from io import BytesIO

def authenticate():
    # Initialize Rekognition client with appropriate authentication mechanism
    return boto3.client('rekognition')

def detect_labels(client, photo, bucket):
    try:
        # Detect labels in the photo
        response = client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
            MaxLabels=10)

        # Print detected labels
        print('Detected labels for ' + photo)
        print()
        for label in response['Labels']:
            print("Label:", label['Name'])
            print("Confidence:", label['Confidence'])
            print()

        return response['Labels']

    except Exception as e:
        print("Error:", e)
        return []

def load_image_from_s3(bucket, photo):
    try:
        # Load the image from S3
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket, photo)
        img_data = obj.get()['Body'].read()
        return Image.open(BytesIO(img_data))

    except Exception as e:
        print("Error loading image from S3:", e)
        return None

def display_image_with_bounding_boxes(img, labels):
    try:
        # Display the image with bounding boxes
        plt.imshow(img)
        ax = plt.gca()
        for label in labels:
            for instance in label.get('Instances', []):
                bbox = instance['BoundingBox']
                left = bbox['Left'] * img.width
                top = bbox['Top'] * img.height
                width = bbox['Width'] * img.width
                height = bbox['Height'] * img.height
                rect = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
                label_text = label['Name'] + ' (' + str(round(label['Confidence'], 2)) + '%)'
                plt.text(left, top - 2, label_text, color='r', fontsize=8, bbox=dict(facecolor='white', alpha=0.7))
        plt.show()

    except Exception as e:
        print("Error displaying image with bounding boxes:", e)

def main():
    try:
        # Specify photo filename and bucket name
        photo = '47a297b3-traffic-light-technology-.jpg'
        bucket = 'aws-rekognition-label-images-shon-102'

        # Authenticate with AWS Rekognition
        client = authenticate()

        # Detect labels in the photo
        labels = detect_labels(client, photo, bucket)

        if labels:
            # Load the image from S3
            img = load_image_from_s3(bucket, photo)

            if img:
                # Display the image with bounding boxes
                display_image_with_bounding_boxes(img, labels)
            else:
                print("Failed to load image from S3.")

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
