const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const icon = (name) => `<svg class="icon"><use href="#i-${name}"></use></svg>`;

const API = {
    baseUrl: "http://localhost:8000",
    chat: "/api/chat",
    timeout: 30000
};

const nav = [
    ["home", "home"],
    ["guide", "chat"],
    ["photo", "camera"],
    ["collection", "archive"],
    ["exhibition", "exhibit"],
    ["service", "clock"],
    ["route", "map"],
    ["history", "bookmark"]
];

const features = [
    ["upload", "camera"],
    ["collection", "archive"],
    ["exhibition", "exhibit"],
    ["service", "clock"]
];

const state = {
    messages: [],
    pending: "",
    request: null,
    seq: 0
};

const esc = (text) => String(text).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
})[char]);

const renderMarkdown = (text) => {
    let html = esc(text);
    html = html.replace(/^####\s+(.+)$/gm, "<h4>$1</h4>");
    html = html.replace(/^###\s+(.+)$/gm, "<h3>$1</h3>");
    html = html.replace(/^---$/gm, "<hr>");
    html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/(?<!\*)\*(.+?)\*(?!\*)/g, "<em>$1</em>");
    html = html.replace(/^\*\s*([^:]+):/gm, "<strong>$1:</strong>");
    html = html.replace(/^(\d+)\.\s+(.+)$/gm, "<li>$2</li>");
    html = html.replace(/(<li>[\s\S]*?<\/li>)/g, "<ul>$1</ul>");
    html = html.replace(/\n/g, "<br>");
    return html;
};

const button = ([key, iconName], extra = "") => `
    <button class="${extra || "nav-item"}" type="button" data-nav="${key}">
        ${icon(iconName)}<span>${currentLocale.get(`nav.${key}`)}</span>
    </button>
`;

function boot() {
    currentLocale.init();
    updateLangButton();
    renderUI();
    bindEvents();
}

function renderUI() {
    $("#navList").innerHTML = nav.map((item, index) => button(item, `nav-item ${index ? "" : "is-active"}`)).join("");
    
    $("#sideLinks").innerHTML = [
        ["feedback", "info", currentLocale.get("actions.feedback")],
        ["settings", "settings", currentLocale.get("actions.settings")]
    ].map(([action, iconName, label]) => `
        <button class="side-link" type="button" data-action="${action}">${icon(iconName)}<span>${label}</span></button>
    `).join("");

    [
        ["#newChatBtn", "chat", currentLocale.get("actions.newChat")],
        ['[data-action="help"]', "info", currentLocale.get("actions.help")],
        ["#uploadBtn", "upload", currentLocale.get("actions.upload")],
        ["#voiceBtn", "mic", currentLocale.get("actions.voice")],
        ["#clearBtn", "trash", currentLocale.get("actions.clear")],
        ["#sendBtn", "send", currentLocale.get("actions.send")]
    ].forEach(([selector, iconName, text]) => {
        $(selector).innerHTML = `${icon(iconName)}${text}`;
    });

    $("#featureGrid").innerHTML = features.map(([key, iconName]) => {
        const feat = currentLocale.get(`features.${key}`);
        return `
            <article class="feature-card">
                <div class="feature-icon">${icon(iconName)}</div>
                <h3>${feat.title}</h3>
                <p>${feat.desc}</p>
                <button class="btn" type="button" data-feature="${key}">${feat.action}</button>
            </article>
        `;
    }).join("");

    const qs = currentLocale.get("questions");
    $("#questionGroups").innerHTML = [
        [currentLocale.get("questionGroups.group1"), qs.slice(0, 4)],
        [currentLocale.get("questionGroups.group2"), qs.slice(4, 8)]
    ].map(([title, items]) => `
        <article class="scenario-card">
            <h2>${title}</h2>
            <ul class="question-list">
                ${items.map((text) => `<li><button class="question-chip" type="button">${icon("search")}${text}</button></li>`).join("")}
            </ul>
        </article>
    `).join("");

    renderEmpty();
    updateStaticText();
}

function updateStaticText() {
    $("#heroTitle").textContent = currentLocale.get("hero.title");
    $(".hero-copy .eyebrow").textContent = currentLocale.get("hero.eyebrow");
    $(".hero-copy p").textContent = currentLocale.get("hero.desc");
    $("#askTitle").innerHTML = `<span>${currentLocale.get("ask.label")}</span><span>${currentLocale.get("ask.hint")}</span>`;
    $("#questionInput").placeholder = currentLocale.get("ask.placeholder");
    $(".section-title h2").textContent = currentLocale.get("featuresTitle");
    $(".section-title p").textContent = currentLocale.get("featuresHint");
    $("#chatTitle").textContent = currentLocale.get("chatTitle");
    $(".chat-head p").textContent = currentLocale.get("chatHint");
    $(".chat-head .badge").innerHTML = `${icon("shield")}${currentLocale.get("badge")}`;
    $(".trust span").textContent = currentLocale.get("trust");
    $(".brand-side strong").textContent = currentLocale.get("brand.side");
    $(".brand-side span").textContent = currentLocale.get("brand.sideSub");
    $(".brand strong").textContent = currentLocale.get("brand.main");
    $(".brand span").textContent = currentLocale.get("brand.mainSub");
}

function updateLangButton() {
    $$(".lang-btn").forEach((btn) => {
        btn.classList.toggle("is-active", btn.textContent.trim() === (currentLocale.lang === "zh" ? "中文" : "English"));
    });
}

function toast(text) {
    const el = $("#toast");
    el.textContent = text;
    el.classList.add("is-visible");
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => el.classList.remove("is-visible"), 1800);
}

function activeNav(key) {
    $$(".nav-item").forEach((item) => item.classList.toggle("is-active", item.dataset.nav === key));
}

function setInput(text, focus = true) {
    $("#questionInput").value = text;
    if (focus) $("#questionInput").focus();
}

function renderEmpty() {
    const empty = currentLocale.get("empty");
    $("#chatFeed").innerHTML = `
        <div class="empty-state">
            <div>
                <div class="empty-icon">${icon("archive")}</div>
                <h3>${empty.title}</h3>
                <p>${empty.desc}</p>
                <div class="source-tags">${empty.tags.map(tag => `<span>${tag}</span>`).join("")}</div>
            </div>
        </div>
    `;
}

function normaliseAnswer(backendResponse, question) {
    if (!backendResponse) return null;

    const responseText = backendResponse.text || currentLocale.get("status.empty.title");
    const metadata = backendResponse.metadata || {};
    const relevantDocs = metadata.relevant_docs || [];
    const firstDoc = relevantDocs.length > 0 ? relevantDocs[0] : null;
    const artifact = metadata.artifact || (firstDoc ? firstDoc.metadata : null);
    const hasArtifact = metadata.has_artifact_card && artifact;

    const answer = currentLocale.get("answer");
    const result = {
        role: "ai",
        title: hasArtifact ? artifact.name : answer.title,
        icon: hasArtifact ? "archive" : answerTypeMeta(question),
        badge: hasArtifact ? answer.artifactBadge : answer.badge,
        conclusion: responseText,
        details: [],
        sources: [],
        imageUrl: hasArtifact ? artifact.image_url : null,
        threeDUrl: hasArtifact ? artifact.three_d_url : null
    };

    if (hasArtifact) {
        const details = currentLocale.get("answer.details");
        const description = firstDoc ? (firstDoc.document.match(/详细描述：([\s\S]*?)(?=\n[^：]+：|\n*$)/) || [])[1] || firstDoc.document || "暂无描述" : "暂无描述";
        result.details = [
            [details.name, artifact.name || "未知"],
            [details.category, artifact.category || "未知"],
            [details.collection, artifact.collection || "未知"],
            [details.era, artifact.era || "未知"],
            [details.description, description.replace(/^\s+|\s+$/g, '')]
        ];
        result.sources = [["馆藏数据库", "文物ID: " + (artifact.artifact_id || artifact.id || "未知")]];
    }

    if (metadata.relevant_docs && metadata.relevant_docs.length > 0) {
        metadata.relevant_docs.forEach(function(doc, index) {
            const meta = doc.metadata || {};
            if (meta.name) {
                result.sources.push(["相关资料" + (index + 1), meta.name || "相关文档"]);
            }
        });
    }

    return result;
}

function answerTypeMeta(question) {
    if (!question) question = "";
    const lang = currentLocale.lang;
    if (lang === "zh") {
        if (question.indexOf("藏品") >= 0 || question.indexOf("文物") >= 0 || question.indexOf("钱币") >= 0 || question.indexOf("馆藏") >= 0) return "archive";
        if (question.indexOf("展览") >= 0 || question.indexOf("特展") >= 0 || question.indexOf("展厅") >= 0) return "exhibit";
        if (question.indexOf("路线") >= 0 || question.indexOf("参观") >= 0 || question.indexOf("顺序") >= 0) return "route";
        if (question.indexOf("开放") >= 0 || question.indexOf("预约") >= 0 || question.indexOf("服务") >= 0 || question.indexOf("时间") >= 0) return "clock";
    } else {
        if (question.indexOf("collection") >= 0 || question.indexOf("artifact") >= 0 || question.indexOf("coin") >= 0 || question.indexOf("treasure") >= 0) return "archive";
        if (question.indexOf("exhibition") >= 0 || question.indexOf("exhibit") >= 0 || question.indexOf("gallery") >= 0) return "exhibit";
        if (question.indexOf("route") >= 0 || question.indexOf("visit") >= 0 || question.indexOf("path") >= 0) return "route";
        if (question.indexOf("open") >= 0 || question.indexOf("reservation") >= 0 || question.indexOf("service") >= 0 || question.indexOf("time") >= 0) return "clock";
    }
    return "chat";
}

async function queryMuseum(question) {
    const controller = new AbortController();
    const timeoutId = setTimeout(function() { controller.abort(); }, API.timeout);
    state.request = controller;

    try {
        const response = await fetch(API.baseUrl + API.chat, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                question: question,
                stream: false,
                language: currentLocale.lang
            }),
            signal: controller.signal
        });

        if (!response.ok) {
            throw new Error("HTTP error! status: " + response.status);
        }

        const data = await response.json();
        return data;
    } finally {
        clearTimeout(timeoutId);
        state.request = null;
    }
}

function getFallbackAnswer(question) {
    const lang = currentLocale.lang;
    
    if (lang === "zh") {
        if (question.indexOf("预约") >= 0 || question.indexOf("参观") >= 0 || question.indexOf("怎么去") >= 0 || question.indexOf("如何") >= 0 || question.indexOf("联系") >= 0) {
            return {
                text: "参观华东师大博物馆无需预约，凭有效证件即可免费入场。团体参观（10人以上）建议提前联系博物馆预约讲解服务。",
                metadata: {}
            };
        } else if (question.indexOf("开放时间") >= 0 || question.indexOf("什么时候") >= 0 || question.indexOf("几点") >= 0 || question.indexOf("闭馆") >= 0) {
            return {
                text: "华东师大博物馆的开放时间为：周二至周日 9:00-17:00（16:30停止入场），周一闭馆。节假日开放时间可能有所调整，请关注官方通知。",
                metadata: {}
            };
        } else if (question.indexOf("展览") >= 0 || question.indexOf("展讯") >= 0 || question.indexOf("活动") >= 0 || question.indexOf("特展") >= 0) {
            return {
                text: "目前华东师大博物馆有多个精彩展览正在进行，包括《历史文物特展》、《生物多样性展》等。您可以通过官网或本系统查询详细展览信息。",
                metadata: {}
            };
        }
        return {
            text: "您好！我是华东师大博物馆的AI导览助手，有什么可以帮助您的吗？您可以询问文物知识、展览信息、参观服务等问题。",
            metadata: {}
        };
    } else {
        if (question.indexOf("reservation") >= 0 || question.indexOf("visit") >= 0 || question.indexOf("how") >= 0 || question.indexOf("contact") >= 0) {
            return {
                text: "No reservation is required for visiting ECNU Museum. Free admission with valid ID. For group visits (10+ people), please contact the museum in advance to book a guided tour.",
                metadata: {}
            };
        } else if (question.indexOf("opening") >= 0 || question.indexOf("when") >= 0 || question.indexOf("time") >= 0 || question.indexOf("close") >= 0) {
            return {
                text: "ECNU Museum is open from Tuesday to Sunday, 9:00-17:00 (last entry at 16:30). Closed on Mondays. Hours may vary during holidays. Please check official announcements.",
                metadata: {}
            };
        } else if (question.indexOf("exhibition") >= 0 || question.indexOf("event") >= 0 || question.indexOf("show") >= 0 || question.indexOf("special") >= 0) {
            return {
                text: "ECNU Museum currently hosts several exhibitions including 'Historical Artifacts Exhibition' and 'Biodiversity Exhibition'. Check the official website or this system for details.",
                metadata: {}
            };
        }
        return {
            text: "Hello! I'm the AI Guide for ECNU Museum. How can I assist you? You can ask about artifacts, exhibitions, visitor services, and more.",
            metadata: {}
        };
    }
}

function sourceHTML(items) {
    if (!items || items.length === 0) return "";
    const answer = currentLocale.get("answer");
    
    var html = `<div class="sources"><h4>${answer.sources}</h4><ul>`;
    items.forEach(function(item) {
        var title = item[0];
        var meta = item[1];
        html += "<li><strong>" + esc(title) + "</strong><span>" + esc(meta) + "</span></li>";
    });
    html += "</ul></div>";
    return html;
}

function answerHTML(answer) {
    var detailsHTML = "";
    if (answer.details && answer.details.length > 0) {
        detailsHTML = "<dl class=\"answer-details\">";
        answer.details.forEach(function(item) {
            var label = item[0];
            var value = item[1];
            detailsHTML += "<div><dt>" + esc(label) + "</dt><dd>" + esc(value) + "</dd></div>";
        });
        detailsHTML += "</dl>";
    }

    var mediaHTML = "";
    if (answer.imageUrl) {
        mediaHTML = `<div class="artifact-image"><img src="${esc(answer.imageUrl)}" alt="${esc(answer.title)}" loading="lazy"></div>`;
    }

    const answerI18n = currentLocale.get("answer");
    var threeDHTML = "";
    if (answer.threeDUrl) {
        threeDHTML = `<div class="three-d-link"><a href="${esc(answer.threeDUrl)}" target="_blank" rel="noopener">${icon("globe")}${answerI18n.threeD}</a></div>`;
    }

    return `
        <article class="answer-card">
            <header class="answer-head">
                <h3>${icon(answer.icon)}${esc(answer.title)}</h3>
                <span class="badge">${esc(answer.badge)}</span>
            </header>
            <div class="answer-body">
                <p>${renderMarkdown(answer.conclusion)}</p>
                ${mediaHTML}
                ${detailsHTML}
                ${threeDHTML}
                ${sourceHTML(answer.sources)}
            </div>
        </article>
    `;
}

function renderChat(extra) {
    if (!extra) extra = "";
    if (!state.messages.length && !extra) return renderEmpty();

    var html = "";
    const assistantName = currentLocale.get("assistant");
    state.messages.forEach(function(msg) {
        if (msg.role === "user") {
            html += "<div class=\"message-row is-user\"><div class=\"message-bubble\">" + esc(msg.text) + "</div></div>";
        } else {
            html += `<div class="message-row is-ai"><div class="message-bubble"><div class="assistant-meta"><img src="logo_museum_official.jpg" alt=""><span>${assistantName}</span></div>${answerHTML(msg)}</div></div>`;
        }
    });

    $("#chatFeed").innerHTML = html + extra;
    $("#chatFeed").scrollTop = $("#chatFeed").scrollHeight;
}

function statusHTML(type) {
    const status = currentLocale.get(`status.${type}`);
    var mark, title, body;

    if (type === "loading") {
        mark = '<span class="spinner" aria-hidden="true"></span>';
        title = status.title;
        body = status.desc;
    } else if (type === "error") {
        mark = icon("info");
        title = status.title;
        body = status.desc + `<br><button class="btn" type="button" data-retry>${currentLocale.get("status.retry")}</button>`;
    } else {
        mark = icon("search");
        title = status.title;
        body = status.desc;
    }

    return "<div class=\"status-card\" role=\"status\">" + mark + "<div><h3>" + title + "</h3><p>" + body + "</p></div></div>";
}

async function ask(text, addUser) {
    if (addUser === undefined) addUser = true;
    const question = text.trim();
    if (!question) {
        toast(currentLocale.get("toast.inputEmpty"));
        return $("#questionInput").focus();
    }

    if (state.request) state.request.abort();
    const seq = ++state.seq;
    state.pending = question;
    $("#questionInput").value = "";
    if (addUser) state.messages.push({ role: "user", text: question });

    renderChat(statusHTML("loading"));

    try {
        let backendResponse;

        try {
            backendResponse = await queryMuseum(question);
        } catch (error) {
            console.log("API调用失败，使用本地兜底回答:", error);
            backendResponse = getFallbackAnswer(question);
        }

        if (seq !== state.seq) return;

        const answer = normaliseAnswer(backendResponse, question);

        if (!answer) return renderChat(statusHTML("empty"));

        state.messages.push(answer);
        renderChat();
    } catch (error) {
        if (seq !== state.seq || error.name === "AbortError") return;
        console.error("聊天失败:", error);
        renderChat(statusHTML("error"));
    }
}

function uploadStatus(stage, text) {
    const el = $("#uploadState");
    el.classList.add("is-visible");
    el.innerHTML = icon("upload") + "<span><strong>" + esc(stage) + "</strong> " + esc(text) + "</span>";
}

async function handleImage(file) {
    const upload = currentLocale.get("upload");
    
    if (!file) return uploadStatus(currentLocale.get("actions.upload"), upload.waiting);
    if (!file.type.startsWith("image/")) return uploadStatus("识别失败", upload.formatError);

    if (state.request) state.request.abort();
    const seq = ++state.seq;
    activeNav("photo");
    uploadStatus(currentLocale.get("actions.upload"), file.name + " " + upload.uploading);
    state.messages.push({ role: "user", text: currentLocale.get("actions.upload") + ": " + file.name });
    renderChat(statusHTML("loading"));
    uploadStatus("识别中", upload.recognizing);

    try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(API.baseUrl + "/api/chat/image-recognition", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("图片识别失败");
        }

        const data = await response.json();
        if (seq !== state.seq) return;

        const answer = normaliseAnswer(data, "图片识别");
        if (!answer) return renderChat(statusHTML("empty"));

        state.messages.push(answer);
        uploadStatus("识别完成", upload.success);
        renderChat();
    } catch (error) {
        console.error("图片识别失败:", error);
        toast(currentLocale.get("toast.inputEmpty"));
        uploadStatus("识别失败", upload.failed);
        renderChat();
    }
}

function resetChat() {
    if (state.request) state.request.abort();
    state.seq += 1;
    state.messages = [];
    state.pending = "";
    $("#questionInput").value = "";
    $("#uploadState").classList.remove("is-visible");
    renderEmpty();
    toast(currentLocale.get("toast.newChat"));
}

function switchLanguage(lang) {
    if (currentLocale.set(lang)) {
        renderUI();
        toast(currentLocale.get("toast.switching"));
    }
}

function bindEvents() {
    $("#sendBtn").addEventListener("click", function() { ask($("#questionInput").value); });
    $("#newChatBtn").addEventListener("click", resetChat);
    $("#voiceBtn").addEventListener("click", function() { toast(currentLocale.get("toast.voiceUnavailable")); });
    $("#clearBtn").addEventListener("click", function() {
        setInput("");
        $("#uploadState").classList.remove("is-visible");
    });
    $("#uploadBtn").addEventListener("click", function() {
        uploadStatus(currentLocale.get("actions.upload"), currentLocale.get("upload.waiting"));
        $("#imageUpload").click();
    });
    $("#imageUpload").addEventListener("change", function(event) {
        handleImage(event.target.files[0]);
        event.target.value = "";
    });
    $("#questionInput").addEventListener("keydown", function(event) {
        if (event.key === "Enter" && (event.metaKey || event.ctrlKey)) ask(event.currentTarget.value);
    });

    document.addEventListener("click", function(event) {
        const question = event.target.closest(".question-chip");
        if (question) return ask(question.textContent.trim());

        const feature = event.target.closest("[data-feature]");
        if (feature) {
            const key = feature.dataset.feature;
            if (key === "upload") return $("#uploadBtn").click();
            activeNav(key);
            return setInput(currentLocale.get(`featurePrompts.${key}`) || "");
        }

        const navItem = event.target.closest("[data-nav]");
        if (navItem) {
            const key = navItem.dataset.nav;
            activeNav(key);
            if (key === "photo") return $("#uploadBtn").click();
            if (key === "home") return window.scrollTo({ top: 0, behavior: "smooth" });
            setInput(currentLocale.get(`featurePrompts.${key}`) || "");
            return toast(currentLocale.get(`featurePrompts.${key}`) ? currentLocale.get("toast.featureQuery") : currentLocale.get("toast.notAvailable"));
        }

        const action = event.target.closest("[data-action]");
        if (action) return toast(action.dataset.action === "help" ? currentLocale.get("toast.helpInfo") : currentLocale.get("toast.notAvailable"));
        if (event.target.closest("[data-retry]") && state.pending) ask(state.pending, false);
    });

    $$(".lang-btn").forEach(function(btn) {
        btn.addEventListener("click", function() {
            const lang = btn.textContent.trim() === "中文" ? "zh" : "en";
            switchLanguage(lang);
        });
    });
}

boot();
