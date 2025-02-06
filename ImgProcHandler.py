from Constants import *
import cv2
import numpy as np

class ImgProcHandler:
    def __init__(self):
        self.cap_front = None
        self.cap_side = None
        self.basket_color_range = (np.array([BASKET_LOW_H, BASKET_LOW_S, BASKET_LOW_V]), np.array([BASKET_HIGH_H, BASKET_HIGH_S, BASKET_HIGH_V]))
        self.ball_red_range1 = (np.array([BALL_RED1_LOW_H, BALL_RED1_LOW_S, BALL_RED1_LOW_V]), np.array([BALL_RED1_HIGH_H, BALL_RED1_HIGH_S, BALL_RED1_HIGH_V]))
        self.ball_red_range2 = (np.array([BALL_RED2_LOW_H, BALL_RED2_LOW_S, BALL_RED2_LOW_V]), np.array([BALL_RED2_HIGH_H, BALL_RED2_HIGH_S, BALL_RED2_HIGH_V]))
        self.ball_blue_range = (np.array([BALL_BLUE_LOW_H, BALL_BLUE_LOW_S, BALL_BLUE_LOW_V]), np.array([BALL_BLUE_HIGH_H, BALL_BLUE_HIGH_S, BALL_BLUE_HIGH_V]))
        self.basket_hight = 0
        self.basket_width = 0
        self.basket_center = None

    def SearchBall(self):
        return
        foundBall = FAIL
        # Read a frame from the front camera
        while (foundBall == FAIL):
            ret, frame = self.cap_front.read()
            if not ret:
                print("Failed to capture frame from front camera.")
                continue
            else:
                h, w = frame.shape[:2]
                new_width = 1200  # Set a new width
                new_height = int(h * (new_width / w))  # Scale height proportionally
                resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
                filtered_frame = self.filter_colors(resized_frame, [self.ball_red_range1, self.ball_red_range2, self.ball_blue_range])
                center = self.find_ball_center(filtered_frame)
                cv2.imshow("Image", filtered_frame)
                cv2.waitKey(1)
        #image_path = "../BigBall.jpg"  # Change to your image path
        #image = cv2.imread(image_path)
        #if image is None:
        #    print("Error: Image not found!")
        #else:
        #    h, w = image.shape[:2]
        #    new_width = 1200  # Set a new width
        #    new_height = int(h * (new_width / w))  # Scale height proportionally
        #    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        #    filtered_image = self.filter_colors(resized_image, [self.ball_red_range1, self.ball_red_range2, self.ball_blue_range])
        #    center = self.find_ball_center(filtered_image)
        #    cv2.imshow("Image", filtered_image)
        #    cv2.waitKey(0)
        #return

    def RecognizeThrow(self):
        print("TODO Recognize Throw")
        return

    def IsScoreFound(self):
        print("TODO Is Score Found")
        return

    def FindBasket(self):
        image_path = "../Basket1.jpeg"  # Change to your image path
        image = cv2.imread(image_path)
        if image is None:
           print("Error: Image not found!")
           return FAIL
        else:
            # Resize image
            h, w = image.shape[:2]
            new_width = 1200  # Set a new width
            new_height = int(h * (new_width / w))  # Scale height proportionally
            resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            # Filter colors
            filtered_image = self.filter_colors(resized_image, [self.basket_color_range])
            #find the basket properties
            self.basket_hight, self.basket_width, self.basket_center = self.FindBoundingBoxToLargestObject(filtered_image)
            if self.basket_hight == 0:
                return FAIL

            # Display the result
            cv2.imshow("Image", filtered_image)
            cv2.waitKey(0)
        return SUCCESS







    def CamConnect(self):
        if Stream_url_front is not None:
            print("trying to connect to camera1")
            self.cap_front = cv2.VideoCapture(Stream_url_front)
            print("finished connecting to camera1")
            if not self.cap_front.isOpened():
                return FAIL

        if Stream_url_side is not None:
            print("trying to connect to camera2")
            self.cap_side = cv2.VideoCapture(Stream_url_side)
            print("finished connecting to camera2")
            if not self.cap_side.isOpened():
                return FAIL
        return SUCCESS

    def Exit(self):
        if self.cap_front is not None:
            self.cap_front.release()
        if self.cap_side is not None:
            self.cap_side.release()
        cv2.destroyAllWindows()

    def filter_colors(self, image, color_ranges):
        """
        Filters an image, keeping only the specified color ranges.

        :param image: Input BGR image.
        :param color_ranges: List of tuples [(lower1, upper1), (lower2, upper2), ...]
                             where lower and upper are numpy arrays defining HSV bounds.
        :return: Filtered image where only the specified colors are preserved.
        """
        # Convert image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create an initial mask of zeros (black image)
        final_mask = np.zeros_like(hsv[:, :, 0], dtype=np.uint8)

        # Stack color masks and use vectorized logical OR
        masks = [cv2.inRange(hsv, lower, upper) for lower, upper in color_ranges]
        final_mask = np.bitwise_or.reduce(masks)  # Faster than looping with bitwise_or

        # Apply mask to original image
        result = cv2.bitwise_and(image, image, mask=final_mask)

        return result

    def find_ball_center(self, filtered_image):
        gray = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=50,
            # param1=50,
            # param2=30,
            param1=30,
            param2=10,
            minRadius=10,
            maxRadius=60
        )

        if circles is not None:
            circles = np.uint16(np.around(circles))
            i = circles[0, 0]
            center = (i[0], i[1])
            radius = i[2]
            cv2.circle(filtered_image, center, 5, (0, 0, 255), -1)
            cv2.circle(filtered_image, center, radius, (0, 255, 0), 3)
            cv2.putText(filtered_image, f"({center[0]},{center[1]})",
                        (center[0] + 10, center[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            return center

        return None

    def FindBoundingBoxToLargestObject(self, image):
        # Convert to grayscale for contour detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find contours
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            print("No basket detected!")
            return 0 ,0 ,0

        # Find the largest contour (assumed to be the basket)
        largest_contour = max(contours, key=cv2.contourArea)

        # Get the bounding rectangle
        x, y, w, h = cv2.boundingRect(largest_contour)

        center = (x + w // 2, y + h // 2)

        # Draw the bounding rectangle and center point (for visualization)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(image, center, 5, (0, 0, 255), -1)

        # Add text with measurements
        cv2.putText(image, f"Width: {w}", (x, y - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, f"Height: {h}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, f"Center: {center}", (x, y + h + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        return h , w, center
