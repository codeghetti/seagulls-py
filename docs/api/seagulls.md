<div>
                ##seagulls
                    The Seagulls Game Engine.

            !!! note "View Source"
    ```python
        &#34;&#34;&#34;
        The Seagulls Game Engine.
        &#34;&#34;&#34;

    ```

    </main>
<script>
    function escapeHTML(html) {
        return document.createElement('div').appendChild(document.createTextNode(html)).parentNode.innerHTML;
    }

    const originalContent = document.querySelector("main.pdoc");
    let currentContent = originalContent;

    function setContent(innerHTML) {
        let elem;
        if (innerHTML) {
            elem = document.createElement("main");
            elem.classList.add("pdoc");
            elem.innerHTML = innerHTML;
        } else {
            elem = originalContent;
        }
        if (currentContent !== elem) {
            currentContent.replaceWith(elem);
            currentContent = elem;
        }
    }

    function getSearchTerm() {
        return (new URL(window.location)).searchParams.get("search");
    }

    const searchBox = document.querySelector(".pdoc input[type=search]");
    searchBox.addEventListener("input", function () {
        let url = new URL(window.location);
        if (searchBox.value.trim()) {
            url.hash = "";
            url.searchParams.set("search", searchBox.value);
        } else {
            url.searchParams.delete("search");
        }
        history.replaceState("", "", url.toString());
        onInput();
    });
    window.addEventListener("popstate", onInput);


    let search, searchErr;

    async function initialize() {
        try {
            search = await new Promise((resolve, reject) => {
                const script = document.createElement("script");
                script.type = "text/javascript";
                script.async = true;
                script.onload = () => resolve(window.pdocSearch);
                script.onerror = (e) => reject(e);
                script.src = "search.js";
                document.getElementsByTagName("head")[0].appendChild(script);
            });
        } catch (e) {
            console.error("Cannot fetch pdoc search index");
            searchErr = "Cannot fetch search index.";
        }
        onInput();

        document.querySelector("nav.pdoc").addEventListener("click", e => {
            if (e.target.hash) {
                searchBox.value = "";
                searchBox.dispatchEvent(new Event("input"));
            }
        });
    }

    function onInput() {
        setContent((() => {
            const term = getSearchTerm();
            if (!term) {
                return null
            }
            if (searchErr) {
                return `<h3>Error: ${searchErr}</h3>`
            }
            if (!search) {
                return "<h3>Searching...</h3>"
            }

            window.scrollTo({top: 0, left: 0, behavior: 'auto'});

            const results = search(term);

            let html;
            if (results.length === 0) {
                html = `No search results for '${escapeHTML(term)}'.`
            } else {
                html = `<h4>${results.length} search result${results.length > 1 ? "s" : ""} for '${escapeHTML(term)}'.</h4>`;
            }
            for (let result of results.slice(0, 10)) {
                let doc = result.doc;
                let url = `${doc.modulename.replaceAll(".", "/")}.html`;
                if (doc.qualname) {
                    url += `#${doc.qualname}`;
                }

                let heading;
                switch (result.doc.type) {
                    case "function":
                        heading = `<span class="def">${doc.funcdef}</span> <span class="name">${doc.fullname}</span><span class="signature">(${doc.parameters.join(", ")})</span>`;
                        break;
                    case "class":
                        heading = `<span class="def">class</span> <span class="name">${doc.fullname}</span>`;
                        break;
                    default:
                        heading = `<span class="name">${doc.fullname}</span>`;
                        break;
                }
                html += `
                        <section class="search-result">
                        <a href="${url}" class="attr ${doc.type}">${heading}</a>
                        <div class="docstring">${doc.doc}</div>
                        </section>
                    `;

            }
            return html;
        })());
    }

    if (getSearchTerm()) {
        initialize();
        searchBox.value = getSearchTerm();
        onInput();
    } else {
        searchBox.addEventListener("focus", initialize, {once: true});
    }

    searchBox.addEventListener("keydown", e => {
        if (["ArrowDown", "ArrowUp", "Enter"].includes(e.key)) {
            let focused = currentContent.querySelector(".search-result.focused");
            if (!focused) {
                currentContent.querySelector(".search-result").classList.add("focused");
            } else if (
                e.key === "ArrowDown"
                && focused.nextElementSibling
                && focused.nextElementSibling.classList.contains("search-result")
            ) {
                focused.classList.remove("focused");
                focused.nextElementSibling.classList.add("focused");
                focused.nextElementSibling.scrollIntoView({
                    behavior: "smooth",
                    block: "nearest",
                    inline: "nearest"
                });
            } else if (
                e.key === "ArrowUp"
                && focused.previousElementSibling
                && focused.previousElementSibling.classList.contains("search-result")
            ) {
                focused.classList.remove("focused");
                focused.previousElementSibling.classList.add("focused");
                focused.previousElementSibling.scrollIntoView({
                    behavior: "smooth",
                    block: "nearest",
                    inline: "nearest"
                });
            } else if (
                e.key === "Enter"
            ) {
                focused.querySelector("a").click();
            }
        }
    });
</script></div>