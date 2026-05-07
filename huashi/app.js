const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const icon = (name) => `<svg class="icon"><use href="#i-${name}"></use></svg>`;

const API = {
    baseUrl: "http://localhost:8000",
    chat: "/api/chat",
    timeout: 30000
};

const nav = [
    ["home", "home", "首页"],
    ["guide", "chat", "AI 导览"],
    ["photo", "camera", "拍照识物"],
    ["collection", "archive", "藏品问答"],
    ["exhibition", "exhibit", "展览信息"],
    ["service", "clock", "参观服务"],
    ["route", "map", "参观路线"],
    ["history", "bookmark", "历史记录"]
];

const featurePrompts = {
    guide: "我想继续和导览台对话，了解博物馆参观建议。",
    photo: "我想上传图片识别相关藏品。",
    collection: "我想按名称、类别、年代或关键词查询馆藏知识。",
    exhibition: "最近有哪些展览？请按展览名称、地点和适合人群整理。",
    service: "博物馆开放时间是什么？参观需要预约吗？",
    route: "请推荐一条适合第一次参观华东师范大学博物馆的路线。",
    history: "查看我之前咨询过的参观服务、藏品和展览问题。"
};

const features = [
    ["upload", "camera", "拍照识物", "上传或拍摄图片，尝试识别相关藏品与背景信息。", "上传图片"],
    ["collection", "archive", "藏品问答", "按名称、类别、年代或关键词查询馆藏知识。", "查询藏品"],
    ["exhibition", "exhibit", "展览信息", "查看当前展览、往期展览与推荐内容。", "查看展览"],
    ["service", "clock", "参观服务", "查询开放时间、预约方式、讲解服务与参观须知。", "查看服务"]
];

const questionGroups = [
    ["参观前想知道", ["博物馆开放时间是什么？", "参观需要预约吗？", "馆内可以拍照吗？", "团体参观怎么预约？"]],
    ["馆藏与展览探索", ["镇馆藏品有哪些？", "最近有哪些展览？", "有哪些适合第一次参观的路线？", "我想了解中国古代钱币相关藏品"]]
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

const button = ([key, iconName, label], extra = "") => `
    <button class="${extra || "nav-item"}" type="button" data-nav="${key}">
        ${icon(iconName)}<span>${label}</span>
    </button>
`;

function boot() {
    $("#navList").innerHTML = nav.map((item, index) => button(item, `nav-item ${index ? "" : "is-active"}`)).join("");
    $("#sideLinks").innerHTML = [
        ["feedback", "info", "反馈问题"],
        ["settings", "settings", "设置"]
    ].map(([action, iconName, label]) => `
        <button class="side-link" type="button" data-action="${action}">${icon(iconName)}<span>${label}</span></button>
    `).join("");

    [
        ["#newChatBtn", "chat", "新对话"],
        ['[data-action="help"]', "info", "帮助"],
        ["#uploadBtn", "upload", "上传图片"],
        ["#voiceBtn", "mic", "语音输入"],
        ["#clearBtn", "trash", "清空"],
        ["#sendBtn", "send", "发送"]
    ].forEach(([selector, iconName, text]) => {
        $(selector).innerHTML = `${icon(iconName)}${text}`;
    });

    $("#featureGrid").innerHTML = features.map(([key, iconName, title, desc, action]) => `
        <article class="feature-card">
            <div class="feature-icon">${icon(iconName)}</div>
            <h3>${title}</h3>
            <p>${desc}</p>
            <button class="btn" type="button" data-feature="${key}">${action}</button>
        </article>
    `).join("");

    $("#questionGroups").innerHTML = questionGroups.map(([title, items]) => `
        <article class="scenario-card">
            <h2>${title}</h2>
            <ul class="question-list">
                ${items.map((text) => `<li><button class="question-chip" type="button">${icon("search")}${text}</button></li>`).join("")}
            </ul>
        </article>
    `).join("");

    bindEvents();
    renderEmpty();
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
    $("#chatFeed").innerHTML = `
        <div class="empty-state">
            <div>
                <div class="empty-icon">${icon("archive")}</div>
                <h3>从一个具体问题开始</h3>
                <p>可询问开放时间、预约方式、展览或藏品，也可以上传图片进行识别。</p>
                <div class="source-tags"><span>馆方知识库</span><span>藏品数据库</span><span>展览资料</span></div>
            </div>
        </div>
    `;
}

function normaliseAnswer(backendResponse, question) {
    if (!backendResponse) return null;

    const responseText = backendResponse.text || "抱歉，没有找到相关信息。";
    const metadata = backendResponse.metadata || {};
    const relevantDocs = metadata.relevant_docs || [];
    const firstDoc = relevantDocs.length > 0 ? relevantDocs[0] : null;
    const artifact = metadata.artifact || (firstDoc ? firstDoc.metadata : null);
    const hasArtifact = metadata.has_artifact_card && artifact;

    const result = {
        role: "ai",
        title: hasArtifact ? artifact.name : "馆方资料查询",
        icon: hasArtifact ? "archive" : answerTypeMeta(question),
        badge: hasArtifact ? "馆方资料" : "资料查询",
        conclusion: responseText,
        details: [],
        sources: [],
        imageUrl: hasArtifact ? artifact.image_url : null,
        threeDUrl: hasArtifact ? artifact.three_d_url : null
    };

    if (hasArtifact) {
        const description = firstDoc ? (firstDoc.document.match(/详细描述：([\s\S]*?)(?=\n[^：]+：|\n*$)/) || [])[1] || firstDoc.document || "暂无描述" : "暂无描述";
        result.details = [
            ["文物名称", artifact.name || "未知"],
            ["类别", artifact.category || "未知"],
            ["所属馆藏", artifact.collection || "未知"],
            ["年代", artifact.era || "未知"],
            ["详细描述", description.replace(/^\s+|\s+$/g, '')]
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
    if (question.indexOf("藏品") >= 0 || question.indexOf("文物") >= 0 || question.indexOf("钱币") >= 0 || question.indexOf("馆藏") >= 0) return "archive";
    if (question.indexOf("展览") >= 0 || question.indexOf("特展") >= 0 || question.indexOf("展厅") >= 0) return "exhibit";
    if (question.indexOf("路线") >= 0 || question.indexOf("参观") >= 0 || question.indexOf("顺序") >= 0) return "route";
    if (question.indexOf("开放") >= 0 || question.indexOf("预约") >= 0 || question.indexOf("服务") >= 0 || question.indexOf("时间") >= 0) return "clock";
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
                stream: false
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
}

function sourceHTML(items) {
    if (!items || items.length === 0) return "";

    var html = "<div class=\"sources\"><h4>来源</h4><ul>";
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

    var threeDHTML = "";
    if (answer.threeDUrl) {
        threeDHTML = `<div class="three-d-link"><a href="${esc(answer.threeDUrl)}" target="_blank" rel="noopener">${icon("globe")}查看3D展示</a></div>`;
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
    state.messages.forEach(function(msg) {
        if (msg.role === "user") {
            html += "<div class=\"message-row is-user\"><div class=\"message-bubble\">" + esc(msg.text) + "</div></div>";
        } else {
            html += "<div class=\"message-row is-ai\"><div class=\"message-bubble\"><div class=\"assistant-meta\"><img src=\"logo_museum_official.jpg\" alt=\"\"><span>华东师范大学博物馆 AI 导览台</span></div>" + answerHTML(msg) + "</div></div>";
        }
    });

    $("#chatFeed").innerHTML = html + extra;
    $("#chatFeed").scrollTop = $("#chatFeed").scrollHeight;
}

function statusHTML(type) {
    var mark, title, body;

    if (type === "loading") {
        mark = '<span class="spinner" aria-hidden="true"></span>';
        title = "正在查询馆方知识库...";
        body = "系统会优先整理馆方资料，并在回答中标明来源。";
    } else if (type === "error") {
        mark = icon("info");
        title = "查询失败，请稍后重试。";
        body = "网络或服务暂时不可用，已保留你的问题。<br><button class=\"btn\" type=\"button\" data-retry>重试</button>";
    } else {
        mark = icon("search");
        title = "没有找到相关馆藏资料，可以换一个关键词试试。";
        body = "建议补充藏品名称、年代、类别、展厅位置或图片。";
    }

    return "<div class=\"status-card\" role=\"status\">" + mark + "<div><h3>" + title + "</h3><p>" + body + "</p></div></div>";
}

async function ask(text, addUser) {
    if (addUser === undefined) addUser = true;
    const question = text.trim();
    if (!question) {
        toast("请输入要查询的问题");
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
    if (!file) return uploadStatus("等待上传", "请选择需要识别的藏品或展品图片。");
    if (!file.type.startsWith("image/")) return uploadStatus("识别失败", "请上传图片格式文件，例如 JPG、PNG 或 HEIC。");

    if (state.request) state.request.abort();
    const seq = ++state.seq;
    activeNav("photo");
    uploadStatus("上传中", file.name + " 正在上传。");
    state.messages.push({ role: "user", text: "上传图片：" + file.name });
    renderChat(statusHTML("loading"));
    uploadStatus("识别中", "正在匹配馆藏资料与展览说明。");

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
        uploadStatus("识别完成", "已找到相关藏品信息。");
        renderChat();
    } catch (error) {
        console.error("图片识别失败:", error);
        toast("图片识别失败，请重试");
        uploadStatus("识别失败", "图片识别服务暂时不可用，您可以尝试文字查询相关藏品。");
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
    toast("已开启新对话");
}

function bindEvents() {
    $("#sendBtn").addEventListener("click", function() { ask($("#questionInput").value); });
    $("#newChatBtn").addEventListener("click", resetChat);
    $("#voiceBtn").addEventListener("click", function() { toast("语音输入暂未开放，请先使用文字查询"); });
    $("#clearBtn").addEventListener("click", function() {
        setInput("");
        $("#uploadState").classList.remove("is-visible");
    });
    $("#uploadBtn").addEventListener("click", function() {
        uploadStatus("等待上传", "请选择需要识别的藏品或展品图片。");
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
            return setInput(featurePrompts[key] || "");
        }

        const navItem = event.target.closest("[data-nav]");
        if (navItem) {
            const key = navItem.dataset.nav;
            activeNav(key);
            if (key === "photo") return $("#uploadBtn").click();
            if (key === "home") return window.scrollTo({ top: 0, behavior: "smooth" });
            setInput(featurePrompts[key] || "");
            return toast(featurePrompts[key] ? "已填入相关查询" : "该入口暂未开放");
        }

        const action = event.target.closest("[data-action]");
        if (action) return toast(action.dataset.action === "help" ? "可从首页问题、功能卡片或输入框开始查询" : "该入口暂未开放");
        if (event.target.closest("[data-retry]") && state.pending) ask(state.pending, false);
    });

    $$(".lang-btn").forEach(function(btn) {
        btn.addEventListener("click", function() {
            $$(".lang-btn").forEach(function(item) { item.classList.remove("is-active"); });
            btn.classList.add("is-active");
            toast(btn.textContent.trim() === "English" ? "English interface is reserved" : "已切换为中文");
        });
    });
}

boot();
