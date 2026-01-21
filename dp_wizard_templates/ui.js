// Wrap in anonymous function to avoid global pollution.
// TODO: Convert to ESM.
(() => {
    const prefix = "celltag_"
    var tags = new Set();
    $(`div[class*='${prefix}']`).each((i, el) => {
        const el_tags = new Set(
            $(el)
            .attr("class")
            .split(" ")
            .filter((class_name) => class_name.startsWith(prefix))
            .map((class_name) => class_name.replace(prefix, ""))
        );
        tags = tags.union(el_tags)
    });

    const options_html = (
        tags
        .values()
        .map((tag) => `<option>${tag}</option>`)
        .toArray()
        .join("\n")
    ) + "<option>(none)</option>";

    $("main").prepend(`
        <div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">
            <div class="jp-Cell-inputWrapper">
                <div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">
                </div>
                <div class="jp-InputArea jp-Cell-inputArea"><div class="jp-InputPrompt jp-InputArea-prompt">
                    Show:
                </div>
                <div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput" data-mime-type="text/markdown">
                    <select>
                        ${options_html}
                    <select>
                </div>
            </div>
        </div>
    `);
})();