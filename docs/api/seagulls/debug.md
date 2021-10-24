<div>
                ##[../seagulls](seagulls).debug
            
            !!! note "View Source"
    ```python
        from ._debug_hud import DebugHud

        __all__ = [
            &#34;DebugHud&#34;,
        ]

    ```

                <section id="DebugHud">
                                <div class="attr class">
        <a class="headerlink" href="#DebugHud">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">DebugHud</span>- seagulls.engine._game_object.GameObject:
    </div>

        !!! note "View Source"
    ```python
        class DebugHud(GameObject):

            _game_clock: GameClock

            def __init__(self, game_clock: GameClock):
                self._game_clock = game_clock
                self._background = Surface((1024, 20))
                self._background.fill((100, 100, 100))
                self._background.set_alpha(100)
                self._font = Font(Path(&#34;assets/fonts/ubuntu-mono-v10-latin-regular.ttf&#34;), 14)

            def tick(self) -&gt; None:
                pass

            def render(self, surface: Surface) -&gt; None:
                fps = str(int(self._game_clock.get_fps())).rjust(3, &#34; &#34;)
                time = self._game_clock.get_time()
                img = self._font.render(
                    f&#34;FPS: {fps} | MS: {time}&#34;,
                    True,
                    (20, 20, 20)
                )
                text_height = img.get_height()
                padding = (self._background.get_height() - text_height) / 2

                surface.blit(self._background, (0, 0))
                surface.blit(img, (10, padding))

    ```

            Interface for anything representing an object in the scene.


                            <div id="DebugHud.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#DebugHud.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">DebugHud</span><span class="signature">(game_clock: <a href="engine.html#_game_clock.GameClock">seagulls.engine._game_clock.GameClock</a>)</span>
    </div>

        !!! note "View Source"
    ```python
            def __init__(self, game_clock: GameClock):
                self._game_clock = game_clock
                self._background = Surface((1024, 20))
                self._background.fill((100, 100, 100))
                self._background.set_alpha(100)
                self._font = Font(Path(&#34;assets/fonts/ubuntu-mono-v10-latin-regular.ttf&#34;), 14)

    ```

    

                            </div>
                            <div id="DebugHud.tick" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#DebugHud.tick">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">tick</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def tick(self) -&gt; None:
                pass

    ```

    

                            </div>
                            <div id="DebugHud.render" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#DebugHud.render">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">render</span><span class="signature">(self, surface: pygame.Surface) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def render(self, surface: Surface) -&gt; None:
                fps = str(int(self._game_clock.get_fps())).rjust(3, &#34; &#34;)
                time = self._game_clock.get_time()
                img = self._font.render(
                    f&#34;FPS: {fps} | MS: {time}&#34;,
                    True,
                    (20, 20, 20)
                )
                text_height = img.get_height()
                padding = (self._background.get_height() - text_height) / 2

                surface.blit(self._background, (0, 0))
                surface.blit(img, (10, padding))

    ```

    

                            </div>
                </section>
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
                script.src = "../search.js";
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
                let url = `../${doc.modulename.replaceAll(".", "/")}.html`;
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