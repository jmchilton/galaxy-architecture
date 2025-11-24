# Client

> 📊 [View as training slides](../../../outputs/training-slides/generated/architecture-client/slides.html)

## Learning Questions
- How is the Galaxy UI built?
- What frontend technologies does Galaxy use?
- How do I develop and test the client?

## Learning Objectives
- Understand the client build process
- Learn about Vue.js and Vuex
- Navigate the client source code
- Run client tests and development servers

## Galaxy Client Architecture

*The architecture of Galaxy's web user interface.*

## Client Architecture

*The architecture of Galaxy's web user interface.*

## Client Directories

- Source JavaScript for the client is in `client/src`.
- Source stylesheets are in `client/src/style`.
- "Packed" bundles served by Galaxy stored in `static/dist`
  - `run.sh` uses `git diff` to try to determine if client needs to be built before starting Galaxy
  - webpack builds these "compiled" artifacts

Upshot - to develop against the client, modify files in `client/` and rebuild with `make client` before
deployment.

## Building the Client - Makefile Targets

```Makefile
client: node-deps ## Rebuild all client-side artifacts (for local dev)
  cd client && yarn run build

client-production-maps: node-deps ## Build optimized artifacts with sourcemaps.
  cd client && yarn run build-production-maps

client-watch: node-deps ## Rebuild client on each change.
  cd client && yarn run watch

client-format: node-deps ## Reformat client code
  cd client && yarn run prettier

client-lint: client-eslint client-format-check ## ES lint and check format of client

client-test: node-deps  ## Run JS unit tests
  cd client && yarn run test

client-test-watch: client ## Watch and run all client unit tests on changes
  cd client && yarn run jest-watch

node-deps: ## Install NodeJS and dependencies.
```

## Automatically Reloading During Development

The following command rebuilds the application on each change.

```
make client-watch
```

This is still a relatively slow process, an extra client development server can be started that proxies non-client requests
to your Galaxy server and selectively reloads only what is needed during active development (hot module replacement or HMR).

```
make client-dev-server
```

Make sure to open Galaxy at [http://localhost:8081](http://localhost:8081) instead to point at the client proxy.

![What is Webpack](../_images/what-is-webpack.svg)

## webpack in Galaxy

Packs and "transpiles" Galaxy ES6 code (.js), Galaxy Vue modules (.vue), libraries from npm, scss stylesheets (.scss) into browser native bundles.

Hundreds of high-level well organized files into optimized single files that can be quickly downloaded.

Lots of active development and complexity around Viz plugins and dependencies for instance, but the webpack configuration file in `config/webpack.config.js` is fairly straightforward.

![Webpack in Action](../_images/jsload.png)

## Stylesheets

- Galaxy shared stylesheets are generally defined using the SCSS syntax
- SCSS is a high-level superset of CSS - [https://sass-lang.com/documentation/syntax](https://sass-lang.com/documentation/syntax)
- `sass` is leveraged by webpack to convert these styles to native CSS at client build time
- Rebuild style with `make style`
- Galaxy's SCSS files can be found in `client/src/style/scss/`

## Package and Build Files

![Client Build Files](../_images/core_files_client_build.mindmap.plantuml.svg)

## Source Files

![Client Build Files](../_images/core_files_client_sources.mindmap.plantuml.svg)

## ES6

The client is built from JavaScript source files. We use ES6 JavaScript.

A tutorial to help learn JavaScript generally might be [https://www.w3schools.com/js/.](https://www.w3schools.com/js/.)

For someone familiar with JavaScript but that wants a primer on the new language features in ES6,
[https://www.w3schools.com/js/js_es6.asp](https://www.w3schools.com/js/js_es6.asp) may be more appropriate.

## Vue

Vue.js is a reactive framework for building web client applications.

We chose Vue.js over React initially because of its focus on allowing developers to incrementally or progressively replace pieces of complex existing applications.

The idea behind Vue.js is fairly simple to pick up and there is a lot of great tutorials and videos available. [https://vuejs.org/v2/guide/](https://vuejs.org/v2/guide/) is a really good jumping off point.

## Pinia

> Pinia is a state management library for Vue.js. It provides stores as the central source of truth, with a simpler, more intuitive API compared to earlier solutions. It supports Vue 2 and Vue 3 with Composition API.

[https://pinia.vuejs.org/](https://pinia.vuejs.org/)

Key features include devtools integration, hot module replacement, type-safe stores, and seamless TypeScript support.

## Client Unit Tests

[https://jestjs.io/](https://jestjs.io/)

Configured in `client/src/jest/jest.config.js`.

Vue tests are placed beside components in `client/src`, more tests in `client/test/qunit/tests` and `client/test/jest/standalone/`.

## Vue Test Utils

> Vue Test Utils is the official unit testing utility library for Vue.js.

[https://vue-test-utils.vuejs.org/](https://vue-test-utils.vuejs.org/)

Really nice reference library documentation. A lot of helpers and concepts to unit test Vue components.

## Client Unit Test Design Tips

[https://github.com/galaxyproject/galaxy/tree/dev/client/docs/src/component-design/unit-testing](https://github.com/galaxyproject/galaxy/tree/dev/client/docs/src/component-design/unit-testing)

- Clearly document the intent of your test
- Implement logic in pure functions when possible
- Wrap native browser resources in a function so they can be easily mocked

## Webhooks in Galaxy

Webhooks is a system in Galaxy which can be used to write small JS and/or Python functions to change predefined locations in the Galaxy client.
<br><br>
In short: A plugin infrastructure for the Galaxy UI


You can learn more about webhooks using our webhook [training]({% link topics/dev/tutorials/webhooks/slides.html %}).

## Webhook masthead example

![A person shaped icon in the Galaxy masthead is being hovered over and the popup reads "Show Username", presumably a custom webhook from a tutorial.](../_images/webhook_masthead.png)

At the header menu: Enabling the overlay search, link to communities ...

You can learn more about webhooks using our webhook [training]({% link topics/dev/tutorials/webhooks/slides.html %}).

## Webhook tool/workflow example

![Screenshot of Galaxy with the job completion screen shown and a PhD comic image shown below.](../_images/webhook_tool.png)

Shown after tool or workflow execution. Comics, citations, support ...

You can learn more about webhooks using our webhook [training]({% link topics/dev/tutorials/webhooks/slides.html %}).

## Webhook history-menu example

![A section of the history menu is labelled Webhooks and shows a custom menu entry.](../_images/webhook_history.png)

Adds an entry to the history menu - no functionality as of now

## Key Takeaways
- Source in `client/src`, built bundles in `static/dist`
- Webpack handles bundling and transpilation
- Vue.js for reactive components
- ES6 JavaScript
- Jest for unit testing
- Webhooks for UI plugins
