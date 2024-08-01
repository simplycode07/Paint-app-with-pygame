import pygame
# from . import settings


class TimeLine:
    def __init__(self):
        self.timeline = []  # list of Events
        self.current_time = 0  # index of current change

    def append(self, drawing_area, change_rect, tool_id):
        surface = pygame.Surface(change_rect.size)
        surface.blit(drawing_area.subsurface(change_rect), (0, 0))
        coordinate = change_rect.topleft
        
        print(f"len: {len(self.timeline)}, time: {self.current_time}")

        if self.current_time < len(self.timeline):
            for _ in range(self.current_time, len(self.timeline)):
                self.timeline.pop(-1)

        if len(self.timeline):
            last_event = self.timeline[-1]
            if tool_id == 0 and last_event.tool_id == 0:
                last_event.add_subevent(surface, coordinate)
                return

        event = Event(surface, coordinate, tool_id)
        self.timeline.append(event)
        self.current_time += 1

    def undo(self, drawing_area):
        if self.current_time > 0:
            self.current_time -= 1
            self.timeline[self.current_time].undo(drawing_area)
        else:
            print("Cannot perform undo")

    def redo(self, drawing_area):
        if self.current_time < len(self.timeline):
            self.timeline[self.current_time].redo(drawing_area)
            self.current_time += 1
        else:
            print("Cannot perform redo")


class Event:
    def __init__(self, surface, coordinate, tool_id):
        self.sub_events = [{"surface":surface, "coordinate":coordinate}]
        self.tool_id = tool_id

    def add_subevent(self, surface, coordinate):
        if self.sub_events[-1]["coordinate"] == coordinate:
            return
        print(f"subevent: {len(self.sub_events)}")
        self.sub_events.append({"surface":surface, "coordinate":coordinate})

    def undo(self, drawing_area):
        # add current state to timeline
        # gotta work on it
        for sub_event in self.sub_events:
            size = sub_event["surface"].get_size()
            coordinate = sub_event["coordinate"]

            rect = pygame.Rect(*size, *coordinate)
            surface = pygame.Surface(size)
            surface.blit(drawing_area.subsurface(rect), (0, 0))

        for i, sub_event in enumerate(self.sub_events):
            print(f"undoing at {i}")
            drawing_area.blit(sub_event["surface"], sub_event["coordinate"])


    def redo(self, drawing_area):
        for i, sub_event in enumerate(self.sub_events):
            print(f"redoing at {i}")
            drawing_area.blit(sub_event["surface"], sub_event["coordinate"])



