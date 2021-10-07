# htmlElements.py
# Author: Marcus D. Bloice <https://github.com/mdbloice>
# Contains dynamic HTML elements that cannot be copied from the resources
# directory, where static HTML and CSS is stored.

class Button():
    def __init__(self, btn_id, btn_label) -> None:
        self.btn_label = btn_label
    def get_html(self):
        return '<a id="%s" class="btn btn-lg btn-default" role="button" style="width: 100px">%s</a>' % (self.btn_id, self.btn_label)


class KeyPressJS():
    def __init__(self, classes) -> None:
        self.classes = classes
    def get_html(self):

        # keyCode values for the following numbers:
        # 1 = 49
        # 2 = 50
        # 3 = 51
        # 4 = 52
        # 5 = 53
        # 6 = 54
        # 7 = 55
        # 8 = 56
        # 9 = 57
        # Therefore the class number + 48
        # This is only to be done for the classes 1-9

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


# Not currently used as we use the static navbar.html file
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
        buttons = []
        post_functions = []
        button_js = []

        for i in range(self.n_classes):
            keyboard_shortcuts.append("<li><kbd>%s</kbd> for <b>%s</b></li>" % (i+1, self.class_names[i]))
            buttons.append('<a id="%s" class="btn btn-lg btn-default" role="button">%s</a>' % (self.class_names[i], self.class_names[i]))
            post_functions.append('$("#%s").click(function () { postToDB(%s); getNewImage(); });' % (self.class_names[i], i))
            button_js.append('$("#%s").click(function () { postToDB(%s, "%s"); getNewImage(); });' % (self.class_names[i], i, self.class_names[i]))

        # Note: % symbols used by Jinja must be escaped as %% or Python
        # string replacements will not function correctly.
        return """
        {%% extends "bootstrap/base.html" %%} {%% set active_page = "index" %%} {%% block
        head %%} {{ super() }}
        <link
        rel="shortcut icon"
        href="{{ url_for('static', filename='favicon.ico') }}"
        />
        {%% endblock %%} {%% block scripts %%} {{ super() }}

        <script>
        const imageURL = "{{ url_for('set_image') }}";

        // NOTE: images|tojson also works, check to see which is better to use.
        // On the server side, we are checking if any of these images have already been labelled and will get a new
        // list on every refresh or page visit.
        var l = JSON.parse('{{ images|tojson|safe }}');
        var count = l.length;

        function getNewImage() {

            // Image are already randomised on the server side, so we simply load them sequentially
            // var randomImage = Math.floor(Math.random() * count);
            // var displayNumber = randomImage + 1;
            // "Image " + displayNumber + " of " + count + " (" + l[randomImage] + ")";

            // Remove first element in the list
            l.shift();

            // Change the image displayed to the user
            document.getElementById("image").src = l[0];

            // Change number of images remaining, labelled, etc.
            var labelled = {{ total_n_images }} - l.length
            var remaining = {{ total_n_images }} - labelled;
            var progressWidthPercent = (((remaining / {{ total_n_images }}) * 100) - 100) * -1;
            var progressPercent = ((labelled / {{ total_n_images }}) * 100).toFixed(1);

            document.getElementById("imageText").innerHTML = "Current image <a href=" + l[0] + " target='_blank'>" + l[0] + "</a>";
            document.getElementById("txtLabelledSoFar").innerHTML = "Labelled: " + labelled;
            document.getElementById("txtRemainingImages").innerHTML = "Remaining: " + remaining;
            document.getElementById("progress-bar").style.width = progressWidthPercent + "%%";
            document.getElementById("progress-bar").innerHTML = progressPercent + "%%"

        }

        function postToDB(taggedAs, labelString) {
            var currentImage = document.getElementById("image").src;
            // split string on the server side, this var contains for example http://127.0.0.1:5000/static/images/9258.jpg when sent
            //var currentImage = currentImage.split("/static/images/")[1];

            const data = {
            image: currentImage,
            label: taggedAs,
            label_string: labelString
            };

            const dataJSON = JSON.stringify(data);

            // jQuery AJAX
            $.ajax({
            type: "POST",
            async: true, // setting to false might be desirable for single user app such as this.
            url: imageURL,
            data: dataJSON,
            error: function (e) {
                console.log(e);
                alert("ERROR: " + e.statusText + "\\nHTTP Status: " + e.status + "\\n\\nData not saved to database!");
            },
            dataType: "json",
            contentType: "application/json",
            });

            console.log(
            "Saved label " + taggedAs + " (" + labelString + ") for " + currentImage +  " to database."
            );

        }

        /*
        $(document).keypress(function (e) {
            // keyCode values for the following characters:
            // 1 = 49
            // 2 = 50
            // 3 = 51
            // keyCode lets you check for the *character* pressed, so Numpad 1
            // is also keyCode 49.
            if (e.keyCode == 49) {
            console.log(
                "Handler for keypress fired with keyCode: " + e.keyCode + " (MALIGNANT)"
            );
            postToDB(1);
            getNewImage();
            } else if (e.keyCode == 50) {
            console.log(
                "Handler for keypress fired with keyCode: " +
                e.keyCode +
                " (INCONCLUSIVE)"
            );
            postToDB(2);
            getNewImage();
            } else if (e.keyCode == 51) {
            console.log(
                "Handler for keypress fired with keyCode: " + e.keyCode + " (BENIGN)"
            );
            postToDB(3);
            getNewImage();
            }
        });
        */

        $(document).ready(function () {
            $("#100pc").click(function () {
            document.getElementById("image").width = "250";
            });

            $("#150pc").click(function () {
            // jQuery styleee
            $("#image")[0].width = "300";
            });

            $("#200pc").click(function () {
            document.getElementById("image").width = "350";
            });

            $("#250pc").click(function () {
            document.getElementById("image").width = "400";
            });

            // Set image to first image in array, whichever that is
            $("#image").attr("src", l[0]);

            // Set number of already labelled items
            // document.getElementById("txtLabelledSoFar").innerHTML = "Total labelled: ";

            $("#currentImageText").attr("href", l[0]);
            document.getElementById("currentImageText").innerHTML = l[0];

            //document.getElementById("currentImageText").innerHTML =
            //"Current image <a href="  " target='_blank'>{{ rand_image }}</a>"

            // Dynamically add JS to save to DB for each class
            %s

        });
        </script>
        {%% endblock %%} {%% block title %%}Labeller{%% endblock %%} {%%
        block content %%} {%% include "navbar.html" %%}

        <div class="container">
        <h1 class="page-header">
            Labeller <small>Image tagging web application</small>
        </h1>
        <div class="row">
            <div class="col-md-4">
            <div class="panel panel-primary" style="background: whitesmoke">
                <div class="panel-heading">Infobox</div>
                <div class="panel-body">
                <h4>Image Details</h4>
                <p id="imageText">
                <!--
                    Image {{ r }} of {{ image_count }} ({{ rand_image }})
                -->
                    Current image <a id="currentImageText" href='' target='_blank'></a>
                </p>
                <hr />

                <h4>Progress</h4>
                <p>Total: {{ total_n_images }}</p>
                <p id="txtLabelledSoFar">Labelled: {{ total_n_images - remaining_image_count }}</p>
                <p id="txtRemainingImages">Remaining: {{ remaining_image_count }}</p>

                <div class="progress">
                    <div
                    class="progress-bar progress-bar-striped progress-bar-animated active"
                    style="width: {{ (((remaining_image_count / total_n_images) * 100) - 100) * -1 }}%%"
                    id="progress-bar"
                    >{{ '%%0.1f' | format(((total_n_images - remaining_image_count) / total_n_images) * 100) }}%%</div>
                </div>

                <hr />

                <h4>Image Size:</h4>
                <center>
                    <div class="btn-group btn-group-toggle" data-toggle="buttons">
                    <label id="100pc" class="btn btn-secondary active">
                        <input
                        type="radio"
                        name="options"
                        id="option1"
                        autocomplete="off"
                        checked
                        />
                        250px
                    </label>
                    <label id="150pc" class="btn btn-secondary">
                        <input
                        type="radio"
                        name="options"
                        id="option2"
                        autocomplete="off"
                        />
                        300px
                    </label>
                    <label id="200pc" class="btn btn-secondary">
                        <input
                        type="radio"
                        name="options"
                        id="option3"
                        autocomplete="off"
                        />
                        350px
                    </label>
                    <label id="250pc" class="btn btn-secondary">
                        <input
                        type="radio"
                        name="options"
                        id="option3"
                        autocomplete="off"
                        />
                        400px
                    </label>
                    </div>
                </center>

                <!--
                <hr />
                <div class="progress">
                    <div
                    class="progress-bar progress-bar-striped"
                    style="width: 0%%"
                    id="accuracy-progress-bar"
                    ></div>
                </div>

                -->

                <hr />
                <h4>Keyboard Shortcuts:</h4>
                <ul>
                    %s
                </ul>
                </div>
            </div>
            </div>
            <div class="col-md-8" align="center">

            <img id="image" width="250px" src="" />

            <hr style="padding: 50px" />
                <div class="btn-group" role="group" aria-label="Class names">
                %s
                </div>
            </div>
        </div>

        </div>

        {%% include "footer.html" %%} {%% endblock %%}
        """ % (' '.join(button_js), ' '.join(keyboard_shortcuts), ' '.join(buttons))