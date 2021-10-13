# htmlElements.py
# Author: Marcus D. Bloice <https://github.com/mdbloice>
# Contains dynamic HTML elements that cannot be copied from the resources
# directory, where static HTML and CSS is stored.
import pkg_resources
import os


class Button():
    def __init__(self, btn_id, btn_label) -> None:
        self.btn_label = btn_label
    def get_html(self):
        return '<a id="%s" class="btn btn-lg btn-default" role="button" style="width: 100px">%s</a>' % (self.btn_id, self.btn_label)


class KeyPressJS():
    def __init__(self, classes) -> None:
        self.classes = classes
    def get_html(self):

        js_elements = []

        l = len(self.classes) if len(self.classes) <= 9 else 10

        for i in range(l):

            js = """
            if (e.keyCode == %s) {
                console.log(
                    "Handler for keypress fired with keyCode: " + e.keyCode + " (%s)"
                );
            postToDB(%s);
            getNewImage();

            """ % ((i+1)+48, self.classes[i], i+1)

            js_elements.append(js)

        return """
        $(document).keypress(function (e) {

            %s

            }
        });
        """ % ' '.join(js_elements)


# Navbar is not currently used as we use the static navbar.html file
# from the package's resources directory.
class Navbar():
    def __init__(self) -> None:
        pass

    def get_html(self) -> str:

        navbar_contents = """
        {% block navbar %}
        <nav class="navbar navbar-default">
            <div class="container-fluid">
                <div class="navbar-header">
                <a class="navbar-brand" href="/"><span class="glyphicon glyphicon-tag"></span> Labeller</a>
                </div>
                <ul class="nav navbar-nav">
                <li class="{{ 'active' if active_page == 'index' else '' }}"><a href="/"><span class="glyphicon glyphicon-home"></span> Label Images</a></li>
                <li class="{{ 'active' if active_page == 'labels' else '' }}"><a href="labels.html"><span class="glyphicon glyphicon-oil"></span> Label Database</a></li>
                <li class="{{ 'active' if active_page == 'about' else '' }}"><a href="about.html"><span class="glyphicon glyphicon-question-sign"></span> About</a></li>
                </ul>
            </div>
        </nav>
        {% endblock %}
        """

        return navbar_contents


class Footer():
    def __init__(self, footerText='Created with <a href="https://github.com/mdbloice/Labeller" target="_blank"><span class="glyphicon glyphicon-tag"></span> Labeller</a>') -> None:
        self.footerText = footerText

    def get_html(self) -> str:
        return """
        <div class="container">
        <hr>
        <footer class="bg-light text-center text-lg-start" style="padding: 10px;">
            <div class="text-center p-3">
            %s
            </div>
        </footer>
        </div>
        """ % self.footerText


class Index():
    def __init__(self, class_names) -> None:
        self.class_names = class_names
        self.n_classes = len(class_names)

    def get_html(self):

        keyboard_shortcuts = []
        keyboard_shortcut_js = []
        buttons = []
        button_js = []

        for i in range(self.n_classes):
            keyboard_shortcuts.append("<li><kbd>%s</kbd> for <b>%s</b></li>" % (i+1, self.class_names[i]))
            keyboard_shortcut_js.append('case "%s": postToDB(%s, "%s"); getNewImage(); break;' % (i+1, i, self.class_names[i]))
            buttons.append('<a id="%s" class="btn btn-lg btn-primary" role="button">%s</a>' % (self.class_names[i], self.class_names[i]))
            button_js.append('$("#%s").click(function () { postToDB(%s, "%s"); getNewImage(); });' % (self.class_names[i], i, self.class_names[i]))

        # Use only the first 10 classes and bind to the keys 1, 2, 3, 4, 5, 6, 7, 8, 9, and 0
        if self.n_classes >= 10:
            keyboard_shortcuts = keyboard_shortcuts[:9]
            keyboard_shortcuts.append("<li><kbd>%s</kbd> for <b>%s</b></li>" % (0, self.class_names[9]))
            keyboard_shortcut_js = keyboard_shortcut_js[:9]
            keyboard_shortcut_js.append('case "%s": postToDB(%s, "%s"); getNewImage(); break;' % (0, 9, self.class_names[9]))

        index_html = pkg_resources.resource_string(__name__, os.path.join('resources', 'index.html')).decode("utf-8")

        return index_html % (' '.join(keyboard_shortcut_js), ' '.join(button_js), ' '.join(keyboard_shortcuts), ' '.join(buttons))
