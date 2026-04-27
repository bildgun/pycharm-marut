import numpy as np
import cv2
webcam = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    #successful_frame_read, frame = webcam.read()
    # hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # #red color
    # red_lower = np.array([136, 87, 111], np.uint8)
    # red_upper = np.array([180, 255, 255], np.uint8)
    # #define mask
    # red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    #
    # #green
    # green_lower = np.array([25,52,72], np.uint8)
    # green_upper = np.array([102,255,255], np.uint8)
    # green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    #
    # #blue
    # blue_lower = np.array([94,80,2], np.uint8)
    # blue_upper = np.array([120,255,255], np.uint8)
    # blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
    #
    # #Dilate
    #
    # # to detect only that particular color
    # kernal = np.ones((26, 26), "uint8")
    #
    # # red color
    # red_mask = cv2.dilate(red_mask, kernal)
    # res_red = cv2.bitwise_and(hsvFrame, hsvFrame, mask=red_mask)
    #
    # # green color
    # green_mask = cv2.dilate(green_mask, kernal)
    # res_green = cv2.bitwise_and(hsvFrame, hsvFrame, mask=green_mask)
    #
    # # blue color
    # blue_mask = cv2.dilate(blue_mask, kernal)
    # res_blue = cv2.bitwise_and(hsvFrame, hsvFrame, mask=blue_mask)
    #
    # # Creating contour to track red color
    # contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 1000):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         if w > 200 and h > 200:
    #             frame = cv2.rectangle(frame, (x, y),
    #                                        (x + w, y + h),
    #                                        (0, 0, 255), 2)
    #
    #             cv2.putText(frame, "Red Colour", (x, y),
    #                         cv2.FONT_HERSHEY_SIMPLEX, 1.0,
    #                         (0, 0, 255))
    #
    # # Creating contour to track green color
    # contours, hierarchy = cv2.findContours(green_mask,
    #                                        cv2.RETR_TREE,
    #                                        cv2.CHAIN_APPROX_SIMPLE)
    #
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 1000):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         if w > 200 and h > 200:
    #             frame = cv2.rectangle(frame, (x, y),
    #                                        (x + w, y + h),
    #                                        (0, 255, 0), 2)
    #
    #             cv2.putText(frame, "Green Colour", (x, y),
    #                         cv2.FONT_HERSHEY_SIMPLEX,
    #                         1.0, (0, 255, 0))
    #
    # # Creating contour to track blue color
    # contours, hierarchy = cv2.findContours(blue_mask,
    #                                        cv2.RETR_TREE,
    #                                        cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 1000):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         if w > 200 and h > 200:
    #             frame = cv2.rectangle(frame, (x, y),
    #                                        (x + w, y + h),
    #                                        (255, 0, 0), 2)
    #
    #             cv2.putText(frame, "Blue Colour", (x, y),
    #                         cv2.FONT_HERSHEY_SIMPLEX,
    #                         1.0, (255, 0, 0))
    ret, frame = webcam.read()
    if not ret:
        break  # Stop if video ends

    # Apply background subtraction
    fgmask = fgbg.apply(frame, learningRate=0.01)
    kernal = np.ones((5, 5), "uint8")
    fgmask = cv2.dilate(fgmask, kernal)
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y),
                                           (x + w, y + h),
                                           (0, 255, 0), 2)

    # Show original and foreground mask side by side
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Foreground Mask', fgmask)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

