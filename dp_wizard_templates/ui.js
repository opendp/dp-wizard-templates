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
    console.log(tags);
})();