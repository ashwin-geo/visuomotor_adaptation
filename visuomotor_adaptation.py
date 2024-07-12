import pygame
import csv
import math
import sys
import pickle
import datetime
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 200

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Visuomotor Adaptation Experiment")
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)


# Load trials from CSV
def load_trials(filename):
    trials = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            trials.append({
                "trial_number": int(row["trial_number"]),
                "angular_displacement": float(row["angular_displacement"]),
                "cursor_visibility": bool(int(row["cursor_visibility"])),
                "target_number": float(row["target_number"])
            })
    return trials


# Draw target
def draw_target(angle):
    x = CENTER[0] + RADIUS * math.cos(math.radians(angle))
    y = CENTER[1] - RADIUS * math.sin(math.radians(angle))
    pygame.draw.circle(screen, RED, (int(x), int(y)), 10)
    return (int(x), int(y))


# Save experiment data to a .pkl file
def save_data(data, participant_id):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_{participant_id}_{timestamp}.pkl"
    filepath = os.path.join('Results', filename)
    with open(filepath, 'wb') as file:
        pickle.dump(data, file)


# Main experiment loop
def run_experiment(trials, participant_id):
    running = True
    trial_index = 0
    clock = pygame.time.Clock()
    experiment_data = []

    while running and trial_index < len(trials):
        trial = trials[trial_index]
        screen.fill(WHITE)
        target_pos = draw_target(trial["target_number"])

        cursor_pos = list(CENTER)
        trial_data = {
            "trial_number": trial["trial_number"],
            "cursor_positions": []
        }

        # Show center of the screen
        pygame.draw.circle(screen, GREEN, CENTER, 10)
        pygame.display.flip()

        # Wait for the participant to bring the cursor to the center
        at_center = False
        while not at_center:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_data(experiment_data, participant_id)
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                break

            mouse_x, mouse_y = pygame.mouse.get_pos()
            distance_to_center = math.hypot(mouse_x - CENTER[0], mouse_y - CENTER[1])
            screen.fill(WHITE)  # Redraw the background
            pygame.draw.circle(screen, BLACK, (CENTER[0], CENTER[1]), int(distance_to_center), 1)
            pygame.draw.circle(screen, GREEN, CENTER, 10)
            pygame.display.flip()

            if distance_to_center < 15:
                at_center = True

        while at_center:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_data(experiment_data, participant_id)
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                break

            # Mouse movement
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle_to_mouse = math.degrees(math.atan2(CENTER[1] - mouse_y, mouse_x - CENTER[0]))
            angle_to_mouse += trial["angular_displacement"]
            distance_to_mouse = math.hypot(mouse_x - CENTER[0], mouse_y - CENTER[1])
            cursor_pos[0] = CENTER[0] + distance_to_mouse * math.cos(math.radians(angle_to_mouse))
            cursor_pos[1] = CENTER[1] - distance_to_mouse * math.sin(math.radians(angle_to_mouse))

            screen.fill(WHITE)
            draw_target(trial["target_number"])

            if trial["cursor_visibility"]:
                pygame.draw.circle(screen, BLUE, (int(cursor_pos[0]), int(cursor_pos[1])), 5)

            pygame.display.flip()
            clock.tick(60)

            trial_data["cursor_positions"].append((cursor_pos[0], cursor_pos[1]))

            if (cursor_pos[0] - target_pos[0]) ** 2 + (
                    cursor_pos[1] - target_pos[1]) ** 2 < 100:  # Target hit condition
                at_center = False
                break

            if distance_to_mouse > RADIUS:  # Target passed
                at_center = False
                break
        experiment_data.append(trial_data)
        trial_index += 1

    save_data(experiment_data, participant_id)
    pygame.quit()


def get_participant_id():
    input_active = True
    participant_id = ""
    while input_active:
        screen.fill(WHITE)
        text_surface = font.render("Enter Participant ID: " + participant_id, True, BLACK)
        screen.blit(text_surface, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    participant_id = participant_id[:-1]
                else:
                    participant_id += event.unicode
    return participant_id


if __name__ == "__main__":
    participant_id = get_participant_id()
    trials = load_trials('trials.csv')
    run_experiment(trials, participant_id)
