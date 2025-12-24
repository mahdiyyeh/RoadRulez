"""
Utility functions for the application.
"""
import os
import math
import pygame


def clear_userdetail_textfile():
    """Deletes everything in the userdetail textfile."""
    with open('userdetails.txt', 'w') as file:
        pass


def is_file_empty():
    """Checks if userdetails file is empty."""
    return os.path.getsize('userdetails.txt') == 0


def clear_window(name_of_window):
    """Clears everything in tkinter window."""
    for widget in name_of_window.winfo_children():
        widget.destroy()


def scale_image(image, scale_factor):
    """Resizes an image based on a scale factor."""
    size = round(image.get_width() * scale_factor), round(image.get_height() * scale_factor)
    return pygame.transform.scale(image, size)


def blit_rotate_centre(screen, image, top_left, angle):
    """Rotates image and assigns new centre so image rotates from centre and not the top left."""
    rotated_image = pygame.transform.rotate(image, angle)
    new_rectangle = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    screen.blit(rotated_image, new_rectangle.topleft)


def write_text_to_centre(screen, font, text, color="#E60000", bg_color="#000000"):
    """Writes text to the centre of the screen."""
    text_bg = font.render(text, True, color, bg_color)
    screen.blit(text_bg, (screen.get_width() / 2 - text_bg.get_width() / 2,
                          screen.get_height() / 2 - text_bg.get_height() / 2))


def bubble_sort(array):
    """Bubble sort algorithm for sorting arrays."""
    length = len(array)
    for i in range(length - 1):
        swapped = False
        for j in range(0, length - i - 1):
            if array[j] > array[j + 1]:
                swapped = True
                array[j], array[j + 1] = array[j + 1], array[j]
        if not swapped:
            return array
    return array


def merge_sort(array):
    """Merge sort algorithm for sorting arrays."""
    if len(array) <= 1:
        return array
    
    mid = len(array) // 2
    left_part = array[:mid]
    right_part = array[mid:]
    
    left_part = merge_sort(left_part)
    right_part = merge_sort(right_part)
    
    return merge(left_part, right_part)


def merge(left, right):
    """Merges two sorted arrays."""
    merged_list = []
    left_num = right_num = 0
    
    while left_num < len(left) and right_num < len(right):
        if left[left_num] < right[right_num]:
            merged_list.append(left[left_num])
            left_num += 1
        else:
            merged_list.append(right[right_num])
            right_num += 1
    
    merged_list.extend(left[left_num:])
    merged_list.extend(right[right_num:])
    
    return merged_list
