def divide_pages_into_parts(pages, parts):
    """
    Divides the total number of pages into the specified number of parts.

    Args:
        pages (int): Total number of pages.
        parts (int): Number of parts to divide the pages into.

    Returns:
        list of tuples: A list where each tuple contains the start and end page numbers for each part.

    Raises:
        TypeError: If 'pages' or 'parts' are not integers.
        ValueError: If 'pages' or 'parts' are not positive integers.
        ValueError: If 'parts' is greater than 'pages'.
    """

    # Error handling
    if not isinstance(pages, int) or not isinstance(parts, int):
        raise TypeError("Both 'pages' and 'parts' must be integers.")

    if pages <= 0 or parts <= 0:
        raise ValueError("'pages' and 'parts' must be positive integers greater than zero.")

    if parts > pages:
        raise ValueError("'parts' cannot be greater than 'pages'.")

    # Calculate the base number of pages per part and the remainder
    pages_per_part = pages // parts
    remainder = pages % parts

    # Initialize variables
    ranges = []
    start_page = 1

    for i in range(parts):
        # Determine the number of pages in this part
        end_page = start_page + pages_per_part - 1

        # Distribute the remainder pages starting from the first part
        if remainder > 0:
            end_page += 1
            remainder -= 1

        # Ensure the end page does not exceed the total number of pages
        if end_page > pages:
            end_page = pages

        # Append the range as a tuple to the list
        ranges.append((start_page, end_page))

        # Update the start page for the next part
        start_page = end_page + 1

    return ranges