-- 测试数据
-- 华东师大博物馆AI智能导览系统

-- 插入用户数据 (密码均为 MD5("123456") = e10adc3949ba59abbe56e057f20f883e)
INSERT INTO `users` (`username`, `password`, `role`) VALUES
('admin', 'e10adc3949ba59abbe56e057f20f883e', 'admin'),
('visitor', 'e10adc3949ba59abbe56e057f20f883e', 'user');

-- 插入文物数据
-- 历史文物馆藏
INSERT INTO `artifacts` (`name`, `description`, `image_url`, `three_d_url`, `category`, `collection`, `era`) VALUES
('大观通宝', '北宋徽宗赵佶铸造的铜钱，钱文为宋徽宗独创的"瘦金体"，书法艺术价值极高。钱币铸造精良，铜质细腻，版别众多，是北宋货币文化的代表之作。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact1.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/1', '古钱币', '古钱币馆', '北宋'),

('王莽货布', '新莽时期铸造的青铜货币，形制独特，文字秀美。王莽篡汉后进行多次货币改革，货布是其中最具代表性的品种之一，体现了新莽时期的政治经济政策。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact2.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/2', '古钱币', '古钱币馆', '新莽'),

('商代青铜矛', '商代晚期青铜武器，造型庄重，纹饰精美。矛身修长，刃部锋利，骹部饰有兽面纹，是研究商代军事装备和青铜铸造工艺的重要实物。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact3.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/3', '青铜器', '历史文物馆', '商代'),

('战国带铭文青铜剑', '战国时期青铜剑，剑身刻有铭文，记载了铸造年代和工匠姓名。剑格装饰精美，刃部保存完好，是研究战国冶金技术和兵器形制的重要文物。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact4.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/4', '青铜器', '历史文物馆', '战国'),

('鎏金铜佛坐像', '北魏时期鎏金青铜佛像，佛像面相端庄慈祥，衣纹流畅自然。表面鎏金保存较好，工艺精湛，体现了古代佛教艺术的最高成就。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact5.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/5', '佛像', '历史文物馆', '北魏'),

('敦煌写经残片', '敦煌莫高窟出土的唐代写经残片，内容为《妙法莲华经》，书法风格遒劲秀丽，具有极高的文献价值和书法艺术价值。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact6.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/6', '书画', '历史文物馆', '唐代'),

('汉代四神规矩镜', '汉代青铜铜镜，镜背饰有四神（青龙、白虎、朱雀、玄武）和规矩纹，构图严谨，铸造精美，是汉代铜镜艺术的代表作。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact7.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/7', '铜镜', '历史文物馆', '汉代'),

('明代一品文官补服', '明清时期官员穿着的补服，胸前绣有仙鹤纹样，代表一品文官。刺绣工艺精湛，色彩鲜艳保存较好，是研究明代官服制度的重要实物。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact8.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/8', '服饰', '历史文物馆', '明代'),

('先秦贝币', '中国最早的货币形态之一，天然海贝经过加工用于商品交换。贝币的出现标志着中国古代货币文化的开端，对后世货币形制影响深远。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact9.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/9', '古钱币', '古钱币馆', '先秦'),

('秦代半两钱', '秦始皇统一六国后发行的铜钱，重量约半两，故名"半两"。钱文为篆书，字体雄浑古朴，是秦代统一货币政策的体现。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact10.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/10', '古钱币', '古钱币馆', '秦代'),

('清代龙洋', '清代光绪年间铸造的银元，正面铸有光绪元宝四字，背面为龙纹图案。龙洋是中国近代机制币的代表，在中国货币史上具有重要地位。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact11.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/11', '古钱币', '古钱币馆', '清代'),

('金代银锭', '金代铸造的银锭，形制规范，铭文清晰。银锭是金代重要的货币形式，反映了金代商品经济的发展水平。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact12.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/12', '古钱币', '古钱币馆', '金代'),

('宋代交子拓片', '北宋时期四川地区发行的纸币"交子"的拓片。交子是世界上最早的纸币之一，它的出现标志着中国乃至世界货币史上的重大变革。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact13.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/13', '古钱币', '古钱币馆', '北宋'),

('战国刀币', '春秋战国时期齐国等地区使用的刀形铜币，形制仿照实际刀具，携带使用方便。刀币是先秦时期重要的金属货币之一。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact14.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/14', '古钱币', '古钱币馆', '战国'),

('战国圜钱', '战国时期秦国等地区使用的圆形铜币，中间有圆孔。圜钱的出现为后来圆形方孔的铜钱形制奠定了基础。', 'https://digitalmuseum.ecnu.edu.cn/images/artifact15.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/15', '古钱币', '古钱币馆', '战国'),

-- 生物标本馆藏
('鸭嘴兽标本', '珍贵的单孔类哺乳动物标本，全国仅三件。鸭嘴兽是进化论的重要证据，具有哺乳动物和爬行动物的双重特征，兼具毒刺和泌乳功能。标本保存完整，形态特征清晰可见。', 'https://digitalmuseum.ecnu.edu.cn/images/specimen1.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/16', '标本', '生物标本馆', '现代'),

('大熊猫标本', '国家一级重点保护动物标本，皮毛保存完好，姿态自然。大熊猫是中国特有的珍稀物种，被誉为"活化石"和"中国国宝"。', 'https://digitalmuseum.ecnu.edu.cn/images/specimen2.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/17', '标本', '生物标本馆', '现代'),

('金丝猴标本', '国家一级重点保护动物标本，又称仰鼻猴。金丝猴是我 国特有的珍稀灵长类动物，毛色金黄鲜艳，具有重要的科研和观赏价值。', 'https://digitalmuseum.ecnu.edu.cn/images/specimen3.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/18', '标本', '生物标本馆', '现代'),

('中华鲟标本', '国家一级重点保护动物标本，又称鳇鱼。中华鲟是长江中最大的鱼类，已有1.4亿年历史，是研究鱼类进化的活化石。', 'https://digitalmuseum.ecnu.edu.cn/images/specimen4.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/19', '标本', '生物标本馆', '现代'),

('玳瑁标本', '国家二级重点保护动物标本，海龟的一种。玳瑁的背甲花纹美丽，自古被视为珍宝，具有重要的文化和收藏价值。', 'https://digitalmuseum.ecnu.edu.cn/images/specimen5.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/20', '标本', '生物标本馆', '现代'),

-- 民俗馆藏
('韩国木雕面具', '韩国传统木雕工艺品的典型代表，用于假面舞等传统表演。面具造型夸张生动，色彩鲜艳，线条流畅，展现了韩国传统木雕艺术的独特魅力。', 'https://digitalmuseum.ecnu.edu.cn/images/folk1.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/21', '民俗工艺品', '海上风民俗博物馆', '现代'),

('泰国丝绸挂毯', '泰国传统手工丝绸制品，采用天然植物染料，色彩艳丽持久。图案多为神话传说和宗教题材，体现了泰国传统纺织工艺的最高水平。', 'https://digitalmuseum.ecnu.edu.cn/images/folk2.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/22', '民俗工艺品', '海上风民俗博物馆', '现代'),

('日本浮世绘', '日本传统木版画艺术，以鲜艳的色彩和细腻的笔触描绘日本民俗风情。浮世绘是了解日本江户时代社会生活的重要窗口。', 'https://digitalmuseum.ecnu.edu.cn/images/folk3.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/23', '民俗工艺品', '海上风民俗博物馆', '现代'),

('越南竹编工艺品', '越南传统竹编技艺制作的工艺品，选用优质竹材，经过多道工序精心编织而成。造型美观大方，具有浓郁的越南民族特色。', 'https://digitalmuseum.ecnu.edu.cn/images/folk4.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/24', '民俗工艺品', '海上风民俗博物馆', '现代'),

('台湾原住民织锦', '台湾少数民族传统织锦工艺品，采用天然纤维手工编织而成，图案多为几何纹样和自然崇拜图案，具有深厚的文化内涵。', 'https://digitalmuseum.ecnu.edu.cn/images/folk5.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/25', '民俗工艺品', '海上风民俗博物馆', '现代'),

('苗族银饰', '苗族传统银饰工艺品的代表，包括银冠、银项圈、银手镯等。银饰做工精细，图案繁复，是苗族文化的重要象征。', 'https://digitalmuseum.ecnu.edu.cn/images/folk6.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/26', '民俗工艺品', '海上风民俗博物馆', '现代'),

('藏族唐卡', '藏族传统宗教绘画艺术品，描绘藏传佛教故事和神祇形象。绘制工艺复杂，使用天然矿物颜料，色彩艳丽持久，具有极高的宗教和艺术价值。', 'https://digitalmuseum.ecnu.edu.cn/images/folk7.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/27', '民俗工艺品', '海上风民俗博物馆', '现代'),

('壮族绣球', '壮族传统手工刺绣工艺品，绣球是壮族青年男女定情信物。刺绣图案精美，色彩鲜艳，寓意吉祥，是壮族民俗文化的重要符号。', 'https://digitalmuseum.ecnu.edu.cn/images/folk8.jpg', 'https://digitalmuseum.ecnu.edu.cn/artifacts/28', '民俗工艺品', '海上风民俗博物馆', '现代');

-- 插入展览数据
INSERT INTO `exhibitions` (`title`, `description`, `start_date`, `end_date`, `location`, `highlights`, `image_url`, `status`) VALUES
('大观通宝钱币专题展', '精选华东师大博物馆藏宋代货币精品，系统展示大观通宝及相关宋代货币的历史背景、铸造工艺和艺术价值。', '2025-03-01', '2025-06-30', '古钱币馆一楼展厅', '镇馆之宝大观通宝、宋代货币演变系列、徽宗御笔亲书展示', 'https://digitalmuseum.ecnu.edu.cn/images/exhibition1.jpg', 'ongoing'),

('生物多样性标本展', '展出华东师大生物标本馆珍藏的国家重点保护动物标本，呼吁公众关注生物多样性保护。', '2025-04-01', '2025-09-30', '生物标本馆主展厅', '鸭嘴兽标本（全国仅三件）、大熊猫、金丝猴、中华鲟等国宝级标本', 'https://digitalmuseum.ecnu.edu.cn/images/exhibition2.jpg', 'ongoing'),

('海上风民俗工艺品展', '来自韩国、泰国、日本、越南、中国台湾等地区的近120件民俗工艺品，展现东亚、东南亚各地区的传统文化魅力。', '2025-02-01', '2025-12-31', '海上风民俗博物馆', '韩国木雕面具、泰国丝绸挂毯、日本浮世绘、越南竹编等特色展品', 'https://digitalmuseum.ecnu.edu.cn/images/exhibition3.jpg', 'ongoing'),

('青铜器纹饰解读展', '系统介绍青铜器上的各种纹饰及其含义，解读商周时期的社会制度和宗教信仰。', '2025-05-01', '2025-08-31', '历史文物馆三楼', '兽面纹、龙纹、凤鸟纹等经典纹饰，青铜器铸造工艺展示', 'https://digitalmuseum.ecnu.edu.cn/images/exhibition4.jpg', 'ongoing'),

('甲骨文与殷商文明', '展示商代甲骨文实物，解读甲骨文记载的殷商历史，展现三千多年前的文明成就。', '2025-06-01', '2025-10-31', '历史文物馆一楼', '珍稀甲骨实物、甲骨文书法艺术、殷商占卜文化解读', 'https://digitalmuseum.ecnu.edu.cn/images/exhibition5.jpg', 'ongoing'),

('中国古代货币文化展', '从先秦贝币到清代龙洋，系统梳理中国三千年的货币发展史，展现货币背后的经济政治变迁。', '2025-07-01', '2025-12-31', '古钱币馆', '先秦贝币、刀币、布币、圜钱系列展示，古代货币铸造工艺体验', 'https://digitalmuseum.ecnu.edu.cn/images/exhibition6.jpg', 'upcoming');

-- 插入咨询记录示例
INSERT INTO `consultations` (`user_id`, `question`, `answer`, `artifact_id`) VALUES
(2, '大观通宝是谁铸造的？', '大观通宝是北宋徽宗赵佶于大观年间（1107-1110年）铸造的铜钱。宋徽宗不仅是一位皇帝，更是一位才华横溢的书法家，他独创的"瘦金体"书法遒劲秀丽，被用于铸刻在大观通宝上，使这枚钱币不仅具有货币功能，更是书法艺术的载体。', 1),
(2, '博物馆今天开门吗？开放时间是什么？', '华东师大博物馆正常开放。周一至周五开放时间为9:00-17:00（16:30停止入馆），周六、周日开放时间为9:00-16:00。节假日开放时间请关注官网公告。建议提前预约参观。', NULL),
(2, '鸭嘴兽标本为什么这么珍贵？', '鸭嘴兽是世界上最珍贵的哺乳动物之一，全国仅存三件完整标本。鸭嘴兽是进化论的重要证据，它同时具有哺乳动物和爬行动物的特征：体温恒定、用乳汁哺育幼儿，但又是卵生动物，爪子间有蹼，还有毒刺。这些独特的特征让它成为科学研究的重要对象。', 16),
(2, '如何预约参观博物馆？', '您可以通过以下方式预约参观：1. 关注华东师范大学博物馆官方微信公众号，在线预约；2. 访问博物馆官网www.digitalmuseum.ecnu.edu.cn进行预约；3. 电话预约：021-xxxx-xxxx。团队参观请提前一周预约。', NULL);

-- 插入搜索统计示例
INSERT INTO `search_stats` (`keyword`, `search_count`) VALUES
('大观通宝', 156),
('鸭嘴兽', 98),
('博物馆开放时间', 87),
('预约参观', 76),
('王莽货布', 65),
('青铜器', 54),
('古钱币', 45),
('标本', 38),
('展览', 32),
('志愿者招募', 28);
