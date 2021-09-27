# htmlElements.py
# Contains dynamic HTML elements that cannot be copied from the resources
# directory, where static HTML and CSS is stored.

class Index():
    def __init__(self) -> None:
        pass

    def get_html(self):
        return """
        {% extends "bootstrap/base.html" %} {% set active_page = "index" %} {% block
        head %} {{ super() }}
        <link
        rel="shortcut icon"
        href="{{ url_for('static', filename='favicon.ico') }}"
        />
        {% endblock %} {% block scripts %} {{ super() }}

        <script>
        const tileURL = "{{ url_for('set_tile') }}";
        const trainLocalModelURL = "{{ url_for('train_local_model') }}";
        const getLatestLossURL = "{{ url_for('get_last_loss') }}";
        const getMetricsURL = "{{ url_for('get_metrics') }}";

        var l = JSON.parse('{{ list_of_tiles|tojson|safe }}');
        var count = l.length;
        //var l = JSON.parse("{{ list_of_tiles|tojson }}");
        var count = l.length;

        function getNewImage() {
            var randomTile = Math.floor(Math.random() * count);
            var displayNumber = randomTile + 1;
            document.getElementById("tileImage").src = l[randomTile];
            document.getElementById("tileText").innerHTML =
            "Tile " + displayNumber + " of " + count + " (" + l[randomTile] + ")";
        }

        function postToDB(taggedAs) {
            var currentImage = document.getElementById("tileImage").src;
            var currentImage = currentImage.split("/tiles/")[1];

            const data = {
            tile: currentImage,
            tag: taggedAs,
            };

            const dataJSON = JSON.stringify(data);

            // jQuery AJAX
            $.ajax({
            type: "POST",
            url: tileURL,
            data: dataJSON,
            error: function (e) {
                console.log(e);
                alert(
                "ERROR: " +
                    e.statusText +
                    "\nHTTP Status: " +
                    e.status +
                    "\n\nData not saved to database!"
                );
            },
            dataType: "json",
            contentType: "application/json",
            });

            console.log(
            "Saved tag " + taggedAs + " for " + currentImage + " to database."
            );

            // Now we update the model with the newly tagged tile
            $.ajax({
            type: "POST",
            url: trainLocalModelURL,
            data: dataJSON,
            // async: false, // very much not liked
            error: function (e) {
                console.log(e);
                alert(
                "ERROR: " +
                    e.statusText +
                    "\nHTTP Status: " +
                    e.status +
                    "\n\nData not passed to model for training!"
                );
            },
            dataType: "json",
            contentType: "application/json",
            });

            console.log(
            "Passed " + currentImage + " with label " + taggedAs + " to local model."
            );

            $.ajax({
            url: getLatestLossURL,
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain; charset=utf-8");
            },
            }).done(function (jsonData) {
            jsonData = JSON.parse(jsonData);
            console.log("Loss reported: " + jsonData.loss);
            document.getElementById("loss-text").innerHTML = "Loss: " + jsonData.loss;
            });

            $.ajax({
            url: getMetricsURL,
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain; charset=utf-8");
            },
            }).done(function (jsonData) {
            jsonData = JSON.parse(jsonData);
            document.getElementById("accuracy-progress-bar").innerText =
                jsonData.data[jsonData.data.length - 1].toFixed(3) * 100 + "%";
            document.getElementById("accuracy-progress-bar").style.width =
                jsonData.data[jsonData.data.length - 1] * 100 + "%";
            document.getElementById("accuracy-text").innerHTML =
                "Accuracy: " + jsonData.data[jsonData.data.length - 1];
            console.log("Passed to accuracy progress bar: " + jsonData.data);
            });
        }

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

        $(document).ready(function () {
            $("#100pc").click(function () {
            document.getElementById("tileImage").width = "224";
            });

            $("#150pc").click(function () {
            // jQuery styleee
            $("#tileImage")[0].width = "336";
            });

            $("#200pc").click(function () {
            document.getElementById("tileImage").width = "448";
            });

            $("#250pc").click(function () {
            document.getElementById("tileImage").width = "560";
            });

            $("#malignant").click(function () {
            postToDB(1);
            getNewImage();
            });

            $("#inconclusive").click(function () {
            postToDB(2);
            getNewImage();
            });

            $("#benign").click(function () {
            postToDB(3);
            getNewImage();
            });

            // Set the loss
            $.ajax({
            url: getLatestLossURL,
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain; charset=utf-8");
            },
            }).done(function (jsonData) {
            jsonData = JSON.parse(jsonData);

            console.log("jsonData.data is: " + jsonData.data);

            if (jsonData.data.length == 0) {
                document.getElementById("loss-text").innerHTML =
                "Loss: Loss appears after first image is tagged";
            } else {
                document.getElementById("loss-text").innerHTML =
                "Loss: " + jsonData.loss;
            }
            });

            // Set the accuracy text string and progress bar, if a test has been performed.
            $.ajax({
            url: getMetricsURL,
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain; charset=utf-8");
            },
            }).done(function (jsonData) {
            jsonData = JSON.parse(jsonData);

            if (jsonData.data.length == 0) {
                document.getElementById("accuracy-text").innerHTML =
                "Accuracy: No tests yet performed.";
            } else {
                document.getElementById("accuracy-text").innerHTML =
                "Accuracy: " + jsonData.data[jsonData.data.length - 1];
            }
            });
        });
        </script>
        {% endblock %} {% block title %}Federated Patho Tile Tagger{% endblock %} {%
        block content %} {% include "navbar.html" %}

        <div class="container">
        <h1 class="page-header">
            Federated Patho Tile Tagger <small>Cross-silo federated learning</small>
        </h1>
        <div class="row">
            <div class="col-md-4">
            <div class="panel panel-primary" style="background: whitesmoke">
                <div class="panel-heading">Options</div>
                <div class="panel-body">
                <h4>Image Details</h4>
                <p id="tileText">
                    Tile {{ r }} of {{ tile_count }} ({{ rand_tile }})
                </p>
                <hr />

                <!--
                <h4>Zoom Level</h4>
                <div class="list-group">
                    <a id="100pcAlt" href="#" class="list-group-item">100%</a>
                    <a id="150pcAlt" href="#" class="list-group-item">150%</a>
                    <a id="200pcAlt" href="#" class="list-group-item">200%</a>
                </div>
                <hr />
                -->

                <h4>Zoom Level:</h4>

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
                        100%
                    </label>
                    <label id="150pc" class="btn btn-secondary">
                        <input
                        type="radio"
                        name="options"
                        id="option2"
                        autocomplete="off"
                        />
                        150%
                    </label>
                    <label id="200pc" class="btn btn-secondary">
                        <input
                        type="radio"
                        name="options"
                        id="option3"
                        autocomplete="off"
                        />
                        200%
                    </label>
                    <label id="250pc" class="btn btn-secondary">
                        <input
                        type="radio"
                        name="options"
                        id="option3"
                        autocomplete="off"
                        />
                        250%
                    </label>
                    </div>
                </center>

                <hr />

                <h4>Metrics</h4>
                <p id="loss-text">Loss: Loss appears after first image is tagged</p>
                <p id="accuracy-text">
                    Accuracy: Accuracy appears after first test set run
                </p>
                <!--


                        <hr>

                        <h4>Local Accuracy:</h4>
                        -->
                <div class="progress">
                    <div
                    class="progress-bar progress-bar-striped"
                    style="width: 0%"
                    id="accuracy-progress-bar"
                    ></div>
                </div>

                <!--
                        <h4>Global Accuracy:</h4>
                        <div class="progress">
                            <div class="progress-bar progress-bar-striped active" style="width:10%;">
                            0%
                            </div>
                        </div>
                        -->

                <hr />
                <h4>Keyboard Shortcuts:</h4>
                <ul>
                    <li><kbd>1</kbd> for <b>Malignant</b></li>
                    <li><kbd>2</kbd> for <b>Inconclusive</b></li>
                    <li><kbd>3</kbd> for <b>Benign</b></li>
                </ul>
                </div>
            </div>
            </div>
            <div class="col-md-8" align="center">
            <img id="tileImage" width="224px" src="{{ rand_tile }}" />
            <hr style="padding: 50px" />
            <a
                id="malignant"
                class="btn btn-lg btn-danger"
                role="button"
                style="width: 100px"
                >1: One</a
            >
            <a
                id="inconclusive"
                class="btn btn-lg btn-default"
                role="button"
                style="width: 100px"
                >2: Two</a
            >
            <a
                id="benign"
                class="btn btn-lg btn-success"
                role="button"
                style="width: 100px"
                >3: Three</a
            >
            </div>
        </div>

        <!---
                <div class="row">
                <div class="col-md-12">
                    <hr>
                    <h3>Keybord shortcuts:</h2>
                    <p>Use <kbd>1</kbd> for <b>Malignant</b>, <kbd>2</kbd> for <b>Inconclusive</b>, and <kbd>3</kbd> for <b>Benign</b>.</p>
                </div>
                </div>
                -->
        </div>

        {% include "footer.html" %} {% endblock %}
        """


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

        _js_elements = []

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

            _js_elements.append(js)

        return """
        $(document).keypress(function (e) {

            %s

            }
        });
        """ % ' '.join(_js_elements)


class Button():
    def __init__(self, btn_label) -> None:
        self.btn_label = btn_label
    def get_html(self):
        return '<a id="malignant" class="btn btn-lg btn-danger" role="button" style="width: 100px">%s</a>' % self.btn_label


class Tags():
    def __init__(self) -> None:
        pass

    def get_html():
        return """
        <html>View Previous Tags Page</html>
        """


class Header():
    def __init__(self) -> None:
        pass

    def get_html(self) -> str:
        return """
        <html>Header</html>
        """

class Navbar():
    def __init__(self) -> None:
        pass

    def get_html(self) -> str:

        navbar_contents = """
        {% block navbar %}
        <nav class="navbar navbar-default">
            <div class="container-fluid">
                <div class="navbar-header">
                <a class="navbar-brand" href="/"><span class="glyphicon glyphicon-cloud"></span> Labeller</a>
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
    def __init__(self, footerText='Created with <a href="https://github.com/mdbloice/Labeller" target="_blank">Labeller</a>') -> None:
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
