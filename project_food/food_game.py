import pygame
import sys
import os


def imageLoader(path, width, height):
    base_path = os.path.dirname(os.path.abspath(__file__))
    image = pygame.image.load(os.path.join(base_path, path))
    return pygame.transform.scale(image, (width, height))


def imageBlit(screen, item, position):
    screen.blit(item, position)


def __main__():
    pygame.init()

    screenHeight = 720
    screenWidth = 1280
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Fest Platter")

    foodItemWidth = 85
    foodItemHeight = 85

    backgroundImage = imageLoader("images/background.jpeg", 1280, 720)
    bananaLeaf = imageLoader("images/bananalf.png", 800, 450)

    # Load images
    rice = imageLoader("images/rice.png", foodItemWidth, foodItemHeight)
    sambar = imageLoader("images/sambar.png", foodItemWidth, foodItemHeight)
    avial = imageLoader("images/avial.png", foodItemWidth, foodItemHeight)
    thoran = imageLoader("images/thoran.png", foodItemWidth, foodItemHeight)
    olan = imageLoader("images/olan.png", foodItemWidth, foodItemHeight)
    kottuCurry = imageLoader("images/kottu_curry.png", foodItemWidth, foodItemHeight)
    erssery = imageLoader("images/erssery.png", foodItemWidth, foodItemHeight)
    pachadi = imageLoader("images/pachadi.png", foodItemWidth, foodItemHeight)
    kichadi = imageLoader("images/kichadi.png", foodItemWidth, foodItemHeight)
    pulissery = imageLoader("images/pulissery.png", foodItemWidth, foodItemHeight)
    injiPuli = imageLoader("images/inji_puli.png", foodItemWidth, foodItemHeight)
    pickles = imageLoader("images/pickle.png", foodItemWidth, foodItemHeight)
    papadem = imageLoader("images/papadem.png", foodItemWidth, foodItemHeight)
    payasam = imageLoader("images/payasam.png", foodItemWidth, foodItemHeight)
    food1 = imageLoader("images/1.png", foodItemWidth, foodItemHeight)
    food2 = imageLoader("images/2.png", foodItemWidth, foodItemHeight)
    food3 = imageLoader("images/3.png", foodItemWidth, foodItemHeight)
    food4 = imageLoader("images/4.png", foodItemWidth, foodItemHeight)
    food5 = imageLoader("images/5.png", foodItemWidth, foodItemHeight)

    # Loaded images to foodPlatter
    foodPlatter = [rice, sambar, avial, thoran, olan, kottuCurry, erssery, pachadi, kichadi, pulissery, injiPuli, pickles, papadem, payasam, food1, food2, food3, food4, food5]

    # Initial positions for draggable items
    initial_positions = [
        (50, 50), (150, 50), (250, 50), (350, 50), (450, 50),
        (550, 50), (650, 50), (750, 50), (850, 50), (950, 50),
        (1050, 50), (1150, 50), (50, 160), (150, 160), (250, 160),
        (350, 160), (450, 160), (550, 160), (650, 160)
    ]

    # Food names
    foodNames = [
        "Rice", "Sambar", "Avial", "Thoran", "Olan",
        "Kottu Curry", "Erssery", "Pachadi", "Kichadi", "Pulissery",
        "Inji Puli", "Pickles", "Papadem", "Payasam", "Mango curry",
        "Paya", "Kola Puttu", "Pulav", "Toudna"
    ]

    # Rect objects for draggable items
    foodRects = []
    for i, (image, name) in enumerate(zip(foodPlatter, foodNames)):
        rect = pygame.Rect(initial_positions[i], (foodItemWidth, foodItemHeight))
        foodRects.append({"image": image, "rect": rect, "name": name, "placed": False})

    # Define positions for placing items on the banana leaf
    banana_leaf_spots = [
        (525, 320), (625, 320), (725, 320), (825, 320), (925, 320),
        (525, 420), (625, 420), (725, 420), (825, 420), (925, 420),
        (525, 520), (625, 520), (725, 520), (825, 520)
    ]

    # Create Rect objects for banana leaf positions
    bananaLeafRects = [pygame.Rect(pos, (foodItemWidth, foodItemHeight)) for pos in banana_leaf_spots]

    # Load result board image
    resultBoardImage = imageLoader("images/onam1.png", 100, 100)

    # Initialize font for timer and food names
    pygame.font.init()
    font = pygame.font.Font(None, 72)  # Larger font size for timer
    small_font = pygame.font.Font(None, 36)  # Smaller font size for food names
    timer_start = pygame.time.get_ticks()
    timer_duration = 60000

    # List to keep track of placed items
    placed_items = []

    # Define correct foods by their indices in the foodPlatter list
    correct_food_indices = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}  # Example indices

    # Initialize health
    health = 3

    dragging = False
    selectedItem = None
    offset_x, offset_y = 0, 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if not dragging:
                    for i, item in enumerate(foodRects):
                        if item["rect"].collidepoint(mouse_x, mouse_y) and not item["placed"]:
                            dragging = True
                            selectedItem = i
                            offset_x = mouse_x - item["rect"].x
                            offset_y = mouse_y - item["rect"].y
                            break

            if event.type == pygame.MOUSEBUTTONUP:
                if dragging and selectedItem is not None:
                    item = foodRects[selectedItem]
                    rect = item["rect"]
                    placed = False
                    for leafRect in bananaLeafRects:
                        if leafRect.colliderect(rect):
                            # Check if the spot is already occupied
                            if not any(leafRect.colliderect(pItem["rect"]) for pItem in placed_items):
                                rect.topleft = leafRect.topleft
                                placed_items.append({"image": item["image"], "rect": rect})
                                item["placed"] = True
                                placed = True
                                # Check if the placed item is correct, if not, decrease health
                                if foodPlatter.index(item["image"]) not in correct_food_indices:
                                    health -= 1  # Decrease health if placed incorrectly
                                break
                    if not placed:
                        rect.topleft = initial_positions[selectedItem]
                    dragging = False
                    selectedItem = None

        if dragging and selectedItem is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rect = foodRects[selectedItem]["rect"]
            rect.topleft = (mouse_x - offset_x, mouse_y - offset_y)

        # Calculate remaining time
        elapsed_time = pygame.time.get_ticks() - timer_start
        remaining_time = max(0, (timer_duration - elapsed_time) // 1000)

        # Render timer
        timer_text = font.render("TIMER", True, (0, 0, 0))  # Black text
        time_value_text = font.render(f"{remaining_time:02d}", True, (0, 0, 0))  # Black text

        screen.blit(backgroundImage, (0, 0))
        screen.blit(bananaLeaf, (350, 250))

        for item in foodRects:
            if not item["placed"]:
                imageBlit(screen, item["image"], item["rect"])

        for item in placed_items:
            imageBlit(screen, item["image"], item["rect"])

        # Draw the timer
        timer_position = (300 - 150, 250 + 225 - 80)  # Adjusted position
        screen.blit(timer_text, timer_position)
        screen.blit(time_value_text, (timer_position[0], timer_position[1] + 50))  # Adjusting position for the timer value

        # Draw health icons based on current health value
        if health == 1:
            imageBlit(screen, resultBoardImage, (50, 600))
        elif health == 2:
            imageBlit(screen, resultBoardImage, (50, 600))
            imageBlit(screen, resultBoardImage, (150, 600))
        elif health >= 3:
            imageBlit(screen, resultBoardImage, (50, 600))
            imageBlit(screen, resultBoardImage, (150, 600))
            imageBlit(screen, resultBoardImage, (250, 600))

        # Display the food name on hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_food = None
        for item in foodRects:
            if item["rect"].collidepoint(mouse_x, mouse_y) and not item["placed"]:
                hovered_food = item["name"]
                break

        if hovered_food:
            name_text = small_font.render(hovered_food, True, (0, 0, 0))  # White text
            screen.blit(name_text, (mouse_x, mouse_y - 30))  # Display above the cursor

        pygame.display.flip()
        clock.tick(60)

        # End game conditions
        if len(placed_items) == 14 or remaining_time == 0 or health <= 0:
            correct_count = sum(1 for item in placed_items if foodPlatter.index(item["image"]) in correct_food_indices)
            total_count = 14
            percentage = (correct_count / total_count) * 100

            # Display the final score
            final_score_text = font.render(f"Score: {percentage:.0f}%", True, (0, 0, 0))
            screen.blit(final_score_text, (850, 160))

            pygame.display.flip()
            pygame.time.wait(3000)
            break  # Pause for a moment to show the result

