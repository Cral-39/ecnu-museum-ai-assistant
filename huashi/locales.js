const locales = {
    zh: {
        nav: {
            home: "首页",
            guide: "AI 导览",
            photo: "拍照识物",
            collection: "藏品问答",
            exhibition: "展览信息",
            service: "参观服务",
            route: "参观路线",
            history: "历史记录"
        },
        features: {
            upload: { title: "拍照识物", desc: "上传或拍摄图片，尝试识别相关藏品与背景信息。", action: "上传图片" },
            collection: { title: "藏品问答", desc: "按名称、类别、年代或关键词查询馆藏知识。", action: "查询藏品" },
            exhibition: { title: "展览信息", desc: "查看当前展览、往期展览与推荐内容。", action: "查看展览" },
            service: { title: "参观服务", desc: "查询开放时间、预约方式、讲解服务与参观须知。", action: "查看服务" }
        },
        featurePrompts: {
            guide: "我想继续和导览台对话，了解博物馆参观建议。",
            photo: "我想上传图片识别相关藏品。",
            collection: "我想按名称、类别、年代或关键词查询馆藏知识。",
            exhibition: "最近有哪些展览？请按展览名称、地点和适合人群整理。",
            service: "博物馆开放时间是什么？参观需要预约吗？",
            route: "请推荐一条适合第一次参观华东师范大学博物馆的路线。",
            history: "查看我之前咨询过的参观服务、藏品和展览问题。"
        },
        questionGroups: {
            group1: "参观前想知道",
            group2: "馆藏与展览探索"
        },
        questions: [
            "博物馆开放时间是什么？",
            "参观需要预约吗？",
            "馆内可以拍照吗？",
            "团体参观怎么预约？",
            "镇馆藏品有哪些？",
            "最近有哪些展览？",
            "有哪些适合第一次参观的路线？",
            "我想了解中国古代钱币相关藏品"
        ],
        actions: {
            feedback: "反馈问题",
            settings: "设置",
            newChat: "新对话",
            help: "帮助",
            upload: "上传图片",
            voice: "语音输入",
            clear: "清空",
            send: "发送"
        },
        empty: {
            title: "从一个具体问题开始",
            desc: "可询问开放时间、预约方式、展览或藏品，也可以上传图片进行识别。",
            tags: ["馆方知识库", "藏品数据库", "展览资料"]
        },
        hero: {
            eyebrow: "高校博物馆数字导览台",
            title: "欢迎来到华东师范大学博物馆 AI 导览台",
            desc: "你可以在这里查询馆藏知识、了解展览信息、咨询开放与预约事项，也可以上传图片尝试识别相关藏品。回答会尽量基于馆方资料生成，请以博物馆官方信息为准。"
        },
        ask: {
            label: "向导览台提问",
            hint: "可咨询开放时间、预约方式、展览、藏品与参观路线",
            placeholder: "试着问：博物馆开放时间是什么？最近有哪些展览？镇馆藏品有哪些？"
        },
        featuresTitle: "请选择要办理的事项",
        featuresHint: "选择事项后，可继续补充日期、关键词或图片。",
        chatTitle: "导览对话",
        chatHint: "每次回答都会尽量标明馆方资料来源。",
        badge: "馆方资料优先",
        trust: "内容由 AI 基于馆方知识库生成，仅供参考；开放时间、预约规则等请以博物馆官方通知为准。",
        toast: {
            switching: "已切换为中文",
            inputEmpty: "请输入要查询的问题",
            newChat: "已开启新对话",
            voiceUnavailable: "语音输入暂未开放，请先使用文字查询",
            featureQuery: "已填入相关查询",
            notAvailable: "该入口暂未开放",
            helpInfo: "可从首页问题、功能卡片或输入框开始查询"
        },
        status: {
            loading: { title: "正在查询馆方知识库...", desc: "系统会优先整理馆方资料，并在回答中标明来源。" },
            error: { title: "查询失败，请稍后重试。", desc: "网络或服务暂时不可用，已保留你的问题。" },
            empty: { title: "没有找到相关馆藏资料，可以换一个关键词试试。", desc: "建议补充藏品名称、年代、类别、展厅位置或图片。" },
            retry: "重试"
        },
        upload: {
            waiting: "请选择需要识别的藏品或展品图片。",
            uploading: "正在上传。",
            recognizing: "正在匹配馆藏资料与展览说明。",
            success: "已找到相关藏品信息。",
            formatError: "请上传图片格式文件，例如 JPG、PNG 或 HEIC。",
            failed: "图片识别服务暂时不可用，您可以尝试文字查询相关藏品。"
        },
        answer: {
            title: "馆方资料查询",
            badge: "资料查询",
            artifactBadge: "馆方资料",
            details: {
                name: "文物名称",
                category: "类别",
                collection: "所属馆藏",
                era: "年代",
                description: "详细描述"
            },
            sources: "来源",
            threeD: "查看3D展示"
        },
        assistant: "华东师范大学博物馆 AI 导览台",
        brand: {
            side: "博物馆导览台",
            sideSub: "游客服务",
            main: "华东师范大学博物馆",
            mainSub: "AI 导览台"
        }
    },
    en: {
        nav: {
            home: "Home",
            guide: "AI Guide",
            photo: "Image Recognition",
            collection: "Collection Q&A",
            exhibition: "Exhibitions",
            service: "Visitor Services",
            route: "Visit Route",
            history: "History"
        },
        features: {
            upload: { title: "Image Recognition", desc: "Upload or take photos to identify related artifacts and background information.", action: "Upload Image" },
            collection: { title: "Collection Q&A", desc: "Search collection knowledge by name, category, era or keywords.", action: "Search Collection" },
            exhibition: { title: "Exhibitions", desc: "View current, past and recommended exhibitions.", action: "View Exhibitions" },
            service: { title: "Visitor Services", desc: "Check opening hours, reservation methods, guided tours and visitor guidelines.", action: "View Services" }
        },
        featurePrompts: {
            guide: "I want to continue the conversation with the guide to get museum visit suggestions.",
            photo: "I want to upload an image to identify related artifacts.",
            collection: "I want to query collection knowledge by name, category, era or keywords.",
            exhibition: "What exhibitions are currently available? Please list them by name, location and target audience.",
            service: "What are the museum opening hours? Do I need to make a reservation?",
            route: "Please recommend a route for first-time visitors to ECNU Museum.",
            history: "View my previously asked questions about visitor services, collections and exhibitions."
        },
        questionGroups: {
            group1: "Before Your Visit",
            group2: "Collections & Exhibitions"
        },
        questions: [
            "What are the museum opening hours?",
            "Do I need to make a reservation?",
            "Can I take photos inside?",
            "How to book group visits?",
            "What are the highlight collections?",
            "What exhibitions are currently on display?",
            "What routes are recommended for first-time visitors?",
            "I want to learn about ancient Chinese coins in the collection"
        ],
        actions: {
            feedback: "Feedback",
            settings: "Settings",
            newChat: "New Chat",
            help: "Help",
            upload: "Upload",
            voice: "Voice Input",
            clear: "Clear",
            send: "Send"
        },
        empty: {
            title: "Start with a specific question",
            desc: "Ask about opening hours, reservations, exhibitions or collections. You can also upload images for identification.",
            tags: ["Official Knowledge Base", "Collection Database", "Exhibition Materials"]
        },
        hero: {
            eyebrow: "University Museum Digital Guide",
            title: "Welcome to ECNU Museum AI Guide",
            desc: "Here you can explore collection knowledge, check exhibition information, inquire about opening hours and reservations, or upload images to identify artifacts. Answers are generated based on official museum information. Please refer to official announcements for confirmation."
        },
        ask: {
            label: "Ask the Guide",
            hint: "Inquire about opening hours, reservations, exhibitions, collections and visit routes",
            placeholder: "Try asking: What are the opening hours? What exhibitions are on display? What are the highlight collections?"
        },
        featuresTitle: "Choose a Service",
        featuresHint: "After selecting a service, you can add dates, keywords or images.",
        chatTitle: "Guide Conversation",
        chatHint: "Each answer will indicate the source of official information.",
        badge: "Official Sources Priority",
        trust: "Content is AI-generated based on the official knowledge base for reference only. Please refer to official museum announcements for opening hours and reservation rules.",
        toast: {
            switching: "Switched to English",
            inputEmpty: "Please enter your question",
            newChat: "New conversation started",
            voiceUnavailable: "Voice input is not available yet. Please use text input.",
            featureQuery: "Query filled in",
            notAvailable: "This feature is not available yet",
            helpInfo: "Start from homepage questions, feature cards or input box"
        },
        status: {
            loading: { title: "Searching museum database...", desc: "The system will prioritize official information and indicate sources in the answer." },
            error: { title: "Query failed, please try again later.", desc: "Network or service temporarily unavailable. Your question has been saved." },
            empty: { title: "No relevant collection information found. Try different keywords.", desc: "Suggest adding artifact name, era, category, exhibition hall location or image." },
            retry: "Retry"
        },
        upload: {
            waiting: "Please select images of artifacts or exhibits to identify.",
            uploading: "Uploading.",
            recognizing: "Matching with collection database and exhibition information.",
            success: "Related artifact information found.",
            formatError: "Please upload image files (JPG, PNG or HEIC).",
            failed: "Image recognition service is temporarily unavailable. Please try text search for related artifacts."
        },
        answer: {
            title: "Official Information",
            badge: "Information Query",
            artifactBadge: "Official Data",
            details: {
                name: "Artifact Name",
                category: "Category",
                collection: "Collection",
                era: "Era",
                description: "Description"
            },
            sources: "Sources",
            threeD: "View 3D Model"
        },
        assistant: "ECNU Museum AI Guide",
        brand: {
            side: "Museum Guide",
            sideSub: "Visitor Services",
            main: "ECNU Museum",
            mainSub: "AI Guide"
        }
    }
};

const currentLocale = {
    lang: "zh",
    get: function(key) {
        const keys = key.split('.');
        let result = locales[this.lang];
        for (const k of keys) {
            result = result?.[k];
            if (result === undefined) return key;
        }
        return result;
    },
    set: function(lang) {
        if (locales[lang]) {
            this.lang = lang;
            document.documentElement.lang = lang;
            localStorage.setItem('locale', lang);
            return true;
        }
        return false;
    },
    init: function() {
        const saved = localStorage.getItem('locale');
        if (saved && locales[saved]) {
            this.lang = saved;
            document.documentElement.lang = saved;
        }
    }
};
