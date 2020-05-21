import sublime, sublime_plugin, re

class ToggleJsExclusiveTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            line = self.view.line(region)
            line_text = self.view.substr(line)

            test_matcher = '(it|describe|test)\('
            exclusive_test_matcher = '(it|describe|test)\.only\('
            match = re.search(exclusive_test_matcher, line_text)

            if match:
                line_without_focus = line_text.replace('.only(', '(')
                self.view.replace(edit, line, line_without_focus)
            else:
                line_with_focus = re.sub(test_matcher, r'\1.only(', line_text)
                self.view.replace(edit, line, line_with_focus)

class ClearJsExclusiveTestsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        matches = []
        results = view.find_all('\.only\(', sublime.IGNORECASE, '(', matches)

        for i, region in reversed(list(enumerate(results))):
          view.replace(edit, region, matches[i])

class ListJsTestsCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        current = view.visible_region()
        regions = view.find_all('^.*(xit|it|xdescribe|describe|test)\(.+[\'"`]', sublime.IGNORECASE)
        lines = list(map(lambda x: view.substr(x) + ')', regions))

        def on_done(i):
            if i == -1:
                view.show_at_center(current)
                return;
            view.sel().clear()
            view.sel().add(regions[i])

        def on_highlighted(i):
            view.show_at_center(regions[i])

        self.window.show_quick_panel(lines, on_done, sublime.MONOSPACE_FONT, 0, on_highlighted)

# class JumpToJsTestCommand(sublime_plugin.TextCommand):
#     def run(self, edit):
#         view = self.view
#         matches = []
#         results = view.find_all('\.only\(', sublime.IGNORECASE, '(', matches)

#         for i, region in reversed(list(enumerate(results))):
#           view.replace(edit, region, matches[i])

#     def find_symbols(self):
#         return [region for region, string in self.view.symbols() if string in ['it', 'describe', 'test']]
