// Wrap in anonymous function to avoid global pollution.
// TODO: Convert to ESM.
(() => {
    const prefix = "celltag_";
    const [tag_map, css_map] = get_maps();
    validate_tags(tag_map);
    insert_html(tag_map);
    insert_css(css_map);

    function get_maps() {
        const $first_cell = $(".jp-Cell").first();
        var frontmatter;
        try {
            frontmatter = JSON.parse($first_cell.text());
        } catch (error) {
            console.warn("First cell can not be parsed as JSON; No further processing.", error);
            return;
        }
        const tag_map = frontmatter?.tag_map;
        const css_map = frontmatter?.css_map;
        if (! (tag_map && css_map)) {
            console.warn("JSON frontmatter missing required elements; No forther processing.", frontmatter);
            return;
        }
        $first_cell.remove();
        return [tag_map, css_map];
    }

    function validate_tags(tag_map) {
        var tags_in_tag_map = new Set();
        Object.values(tag_map).forEach((tags) => {
            tags.forEach((tag) => {
                tags_in_tag_map.add(tag)
            })
        });
        var tags_on_cells = new Set();
        $(`div[class*='${prefix}']`).each((i, el) => {
            $(el)
                .attr("class")
                .split(" ")
                .filter((class_name) => class_name.startsWith(prefix))
                .map((class_name) => class_name.replace(prefix, ""))
                .forEach((tag) => {
                    tags_on_cells.add(tag);
                });
        });
        // Latest JS standard has more Set methods,
        // but this has wider browser support.
        // TODO: better solution.
        const tag_map_string = Array.from(tags_in_tag_map).sort().join(", ")
        const cells_string = Array.from(tags_on_cells).sort().join(", ")
        if (tag_map_string !== cells_string) {
            console.warn(
                "Check for tag typos.\nIn tag_map:", tag_map_string,
                "\nOn cells:", cells_string,
            );
        }
    }

    function show_only(tags) {
        // Substring match ("*=")is slightly too general, but unlikely to matter.
        // The DOM for markdown and code cells is different:
        // Markdown cells are deeply nested, so we use ":has()".
        $(`.jp-Cell[class*="${prefix}"]`).hide();
        $(`.jp-Cell:has([class*="${prefix}"])`).hide();
        tags.forEach((tag) => {
            const tag_css = `.${prefix}${tag}`;
            $(`.jp-Cell${tag_css}`).show();
            $(`.jp-Cell:has(${tag_css})`).show()
        });
    }

    function insert_html(tag_map) {
        const $select = $("<select>");
        const delim = "|";
        Object.entries(tag_map).forEach(([label, tags]) => {
            $select.append($("<option>", {value: tags.join(delim)}).text(label));
        });

        // HTML skeleton is just copy-paste from notebook source:
        // Looks ok, but the semantics aren't correct.
        $("main").prepend(`
            <div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">
                <div class="jp-Cell-inputWrapper">
                    <div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">
                    </div>
                    <div class="jp-InputArea jp-Cell-inputArea"><div class="jp-InputPrompt jp-InputArea-prompt">
                        Show:
                    </div>
                    <div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput" data-mime-type="text/markdown">
                        <select>${$select.html()}</select>
                    </div>
                </div>
            </div>
        `);

        const default_tags = Object.values(tag_map)[0];
        show_only(default_tags);

        $("select").on("change", (event) => {
            const tags = event.target.value.split(delim);
            show_only(tags);
        })
    }

    function insert_css(css_map) {
        const rules = Object.entries(css_map).map(
            ([tag, css]) =>
                `.jp-Cell:has(.celltag_${tag}), .celltag_${tag} {${css}}`
        );
        $("head").append(`<style>${rules.join("\n")}</style>`);
    }
})();