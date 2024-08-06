import pygame
from . import colors
# from . import settings


class TimeLine:
    def __init__(self):
        self.timeline = []  # list of Events
        self.current_time = 0  # index of current change

    def append(self, drawing_area, change_rect, tool_id):
        change_rect = change_rect.clip(drawing_area.get_rect())
        surface = pygame.Surface(change_rect.size)

        if tool_id != 3:
            surface.blit(drawing_area.subsurface(change_rect), (0, 0))
        else:
            surface.blit(drawing_area, (0, 0))

        coordinate = change_rect.topleft

        print(f"len: {len(self.timeline)}, time: {self.current_time}")

        if self.current_time < len(self.timeline):
            for _ in range(self.current_time, len(self.timeline)):
                self.timeline.pop(-1)

        if len(self.timeline):
            last_event = self.timeline[-1]
            if tool_id == 0 and last_event.tool_id == 0 and not last_event.stroke_end:
                last_event.add_subevent(surface, coordinate)
                return

            last_event_coordinates = last_event.rev_sub_events[-1]["coordinate"]
            last_event_surface_size = last_event.rev_sub_events[-1]["surface"].get_size(
            )
            if last_event_coordinates == coordinate and last_event_surface_size == surface.get_size():
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

    def get_last_event(self):
        if len(self.timeline):
            return self.timeline[-1]
        else:
            return None

    def end_stroke(self):
        last_event = self.get_last_event()
        if last_event:
            last_event.stroke_end = True

    def reset(self):
        self.timeline = []
        self.current_time = 0


class Event:
    def __init__(self, surface, coordinate, tool_id):
        self.rev_sub_events = [{"surface": surface, "coordinate": coordinate}]
        self.forw_sub_events = []
        self.tool_id = tool_id
        self.stroke_end = False

    def add_subevent(self, surface, coordinate):
        print(f"subevent: {len(self.rev_sub_events)}")
        self.rev_sub_events.append({"surface": surface, "coordinate": coordinate})

    def undo(self, drawing_area):
        # add current state to timeline
        # gotta work on it
        for rev_sub_event in reversed(self.rev_sub_events):
            size = rev_sub_event["surface"].get_size()
            coordinate = rev_sub_event["coordinate"]

            rect = pygame.Rect(*coordinate, *size)
            surface = pygame.Surface(size)

            if self.tool_id != 3:
                surface.blit(drawing_area.subsurface(rect), (0, 0))

            else:
                surface.blit(drawing_area, (0, 0))
            
            self.forw_sub_events.append({"surface":surface, "coordinate":coordinate})

        for rev_sub_event in reversed(self.rev_sub_events):
            drawing_area.blit(rev_sub_event["surface"], rev_sub_event["coordinate"])

    # gotta work on it

    def redo(self, drawing_area):
        for forw_sub_event in self.forw_sub_events:
            drawing_area.blit(
                forw_sub_event["surface"], forw_sub_event["coordinate"])
