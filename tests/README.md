`test_index_html.py` is weird!

It doesn't contain any unit tests, per se, but it is executed as part of test discovery.
Besides making assertions about the results of template fills,
it runs itself through `convert_nb_to_html`, and updates the Github Pages `index.html`.
If there are changes, it will fail... but the next test run will pass.