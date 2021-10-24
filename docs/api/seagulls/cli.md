<div>
                ##[../seagulls](seagulls).cli
            
            !!! note "View Source"
    ```python
        from ._main import main
        from ._next import cli_next

        __all__ = [
            &#34;main&#34;,
            &#34;cli_next&#34;,
        ]

    ```

                <section id="main">
                            <div class="attr function"><a class="headerlink" href="#main">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">main</span><span class="signature">()</span>:
    </div>

        !!! note "View Source"
    ```python
        def main():
            # Got tired of running into exceptions when this isn&#39;t initialized in time.
            pygame.init()

            logging_verbosity = int(os.environ.get(&#34;VERBOSITY&#34;, &#34;3&#34;))
            if &#34;DEBUG&#34; in os.environ:
                logging_verbosity = 100  # 100 is higher than any log level we will ever have

            di_container = SeagullsDiContainer(_logging_verbosity=logging_verbosity)
            logging_client = di_container.logging_client()
            logging_client.configure_logging()

            root_command = di_container.root_command()

            # Build the CLI Command Interface
            parser = ArgumentParser(
                description=root_command.get_command_help(),
            )
            parser.set_defaults(cmd=root_command)
            parser.set_defaults(parser=parser)

            root_command.configure_parser(parser)

            sub_commands = parser.add_subparsers(title=&#34;subcommands&#34;, metavar=None, help=&#34;&#34;)

            for provider in di_container.traverse():
                provided = provider.provides
                try:
                    is_command = issubclass(provided, CliCommand)
                except TypeError:
                    continue

                if not is_command:
                    continue

                logger.info(f&#34;Initializing CliCommand: {provided}&#34;)
                cmd: CliCommand = provider()
                subparser = sub_commands.add_parser(
                    name=cmd.get_command_name(),
                    help=cmd.get_command_help(),
                )
                cmd.configure_parser(subparser)
                subparser.set_defaults(cmd=cmd)

            args = parser.parse_args(sys.argv[1:])
            matched_cmd: CliCommand = args.cmd
            matched_cmd.execute(vars(args))

    ```

    

                </section>
                <section id="cli_next">
                            <div class="attr function"><a class="headerlink" href="#cli_next">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">cli_next</span><span class="signature">()</span>:
    </div>

        !!! note "View Source"
    ```python
        def cli_next():
            # Got tired of running into exceptions when this isn&#39;t initialized in time.
            pygame.init()

            logging_verbosity = int(os.environ.get(&#34;VERBOSITY&#34;, &#34;3&#34;))
            if &#34;DEBUG&#34; in os.environ:
                logging_verbosity = 100  # 100 is higher than any log level we will ever have

            di_container = SeagullsDiContainer(_logging_verbosity=logging_verbosity)
            logging_client = di_container.logging_client()
            logging_client.configure_logging()

            root_command = di_container.root_command()

            # # Build the CLI Command Interface
            # parser = ArgumentParser(
            #     description=root_command.get_command_help(),
            # )
            # parser.set_defaults(cmd=root_command)
            # parser.set_defaults(parser=parser)
            #
            # root_command.configure_parser(parser)
            #
            # sub_commands = parser.add_subparsers(title=&#34;subcommands&#34;, metavar=None, help=&#34;&#34;)
            #
            # for provider in di_container.traverse():
            #     provided = provider.provides
            #     try:
            #         is_command = issubclass(provided, CliCommand)
            #     except TypeError:
            #         continue
            #
            #     if not is_command:
            #         continue
            #
            #     logger.info(f&#34;Initializing CliCommand: {provided}&#34;)
            #     cmd: CliCommand = provider()
            #     subparser = sub_commands.add_parser(
            #         name=cmd.get_command_name(),
            #         help=cmd.get_command_help(),
            #     )
            #     cmd.configure_parser(subparser)
            #     subparser.set_defaults(cmd=cmd)
            #
            # args = parser.parse_args(sys.argv[1:])
            # matched_cmd: CliCommand = args.cmd
            # matched_cmd.execute(vars(args))

    ```

    

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