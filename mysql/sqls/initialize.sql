CREATE DATABASE anime_recommender;
USE anime_recommender

-- MariaDB dump 10.19  Distrib 10.6.4-MariaDB, for debian-linux-gnu (aarch64)
--
-- Host: 172.30.0.2    Database: anime_recommender
-- ------------------------------------------------------
-- Server version	10.6.4-MariaDB-1:10.6.4+maria~focal

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `anime_data`
--

DROP TABLE IF EXISTS `anime_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anime_data` (
  `anime_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `image` varchar(127) DEFAULT NULL,
  `description` text NOT NULL,
  `year` varchar(127) NOT NULL,
  `genre` varchar(255) NOT NULL,
  `company` varchar(255) NOT NULL,
  PRIMARY KEY (`anime_id`),
  UNIQUE KEY `anime_id` (`anime_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anime_data`
--

LOCK TABLES `anime_data` WRITE;
/*!40000 ALTER TABLE `anime_data` DISABLE KEYS */;
INSERT INTO `anime_data` VALUES (1,'アーヤと魔女','NULL','ダイアナ・ウィン・ジョーンズによるファンタジー小説、またそれを原作としたスタジオジブリ制作のアニメーション作品。','2020','ファンタジー','スタジオジブリ\r'),(2,'五等分の花嫁','gotoubunn.jpg','春場ねぎによる日本の漫画作品。','2019','ラブコメディ','手塚プロダクション\r'),(3,'PSYCHO-PASS サイコパス 3','psychopass3.jpeg','Production I.G制作による日本のオリジナルテレビアニメ作品、および、これを原作としたメディアミックス作品。','2019秋','SF アクション クライムサスペンス','ProductionI.G\r'),(4,'鬼滅の刃','kimetsunoyaiba.png','大正時代を舞台に主人公が鬼と化した妹を人間に戻す方法を探すために戦う姿を描く和風剣戟奇譚。','2019','剣劇 ダーク・ファンタジー','ufotable\r'),(5,'呪術廻戦','jujutukaisen.jpeg','人間の負の感情から生まれる化け物・呪霊を呪術を使って祓う呪術師の闘いを描いた、ダークファンタジー・バトル漫画。','2020秋','ダーク・ファンタジー','MAPPA\r'),(6,'進撃の巨人','shingeki.png','圧倒的な力を持つ巨人とそれに抗う人間達との戦いを描いたダーク・ファンタジー漫画。','2017','ダークファンタジー アクション','MAPPA\r'),(7,'ノラと皇女と野良猫ハート','noratokoujoto.jpg','日本のアダルトゲームブランドであるHARUKAZEより2016年2月26日に発売された成人向け美少女ゲーム原作。地上世界に住むごく普通の少年・ノラが、冥界の皇女・パトリシアの魔法によって猫の姿にされてしまうというファンタジー作品。','2017夏','恋愛 学園 ファンタジー','ダブトゥーンスタジオ\r'),(8,'京都寺町三条のホームズ','kyototeramachisanjo.png','京都へ移り住んで半年になる女子高生の真城葵は、とある事情により亡き祖父の骨董品を鑑定してもらうべく、寺町三条商店街にポツリと佇む骨董品店『蔵』を訪れる。しかしそこで出逢った鑑定士の家頭清貴は美形で上品で柔らかな物腰でありながら、実は「ホームズ」の異名で呼ばれるほど怖ろしく鋭い人物で、葵が骨董品を家族に内緒でこっそり持ち出してきたことをその場で見抜いてしまう。どうしてもお金が必要だった葵に、清貴は『蔵』でアルバイトをしてはどうかと持ち掛け、その日から葵は彼と共に骨董品と京都にまつわる様々な出来事に遭遇していくことに。','2018夏','ミステリー','アニメーションスタジオ・セブン\r'),(9,'SSSS.GRIDMAN','gridman.jpg','響裕太はある日、クラスメイトの宝多六花の家の前で倒れ、自分の名前を含むすべての記憶を思いだせない状態で目覚める。混乱する裕太は、六花の家が営むジャンクショップに置かれていた古いパソコンから呼びかけて来るハイパーエージェントグリッドマンから、自身の使命を果たすように諭される。裕太は戸惑いながらも日常生活に戻るが、街に謎の怪獣が現れたとき、グリッドマンに導かれるまま彼と合体して怪獣を撃破する。かくして裕太は、六花や友人の内海将とグリッドマン同盟を結成し、怪獣の脅威に立ち向かう。','2018秋','SF','TRIGGER\r'),(10,'ゴールデンカムイ','goldenkamui.jpg','明治末期、日露戦争終結直後の北海道周辺を舞台とした、金塊をめぐるサバイバルバトル漫画。また戊辰戦争・日露戦争・ロシア革命などの歴史ロマン要素のほか、狩猟・グルメ要素、アイヌなどの民俗文化の紹介要素も併せ持つ。','2018/2020','冒険 歴史 青年漫画','ジェノスタジオ\r'),(11,'ご注文はうさぎですか？','gochiusa.jpg','高校入学を機に「木組みの家と石畳の街」に引っ越してきたココア。下宿先を探しつつ休憩がてら喫茶店に入ると、偶然にもそこが自分の下宿先ラビットハウスであった。ココアは、お世話になる家に奉仕をするという高校の方針により、ラビットハウスの店員として、そしてラビットハウスの一人娘であるチノの“自称”姉として働くことになるのであった。','2014','日常','WHITE FOX\r'),(12,'銀魂','gintama.jpg','宇宙の知的生物天人（あまんと）諸族によって開国を強要され、銀河文明が導入された江戸のかぶき町を主たる舞台とする物語である。','2011-2018','SF 時代劇 ギャグ','サンライズ\r'),(13,'PUI PUI モルカー','molcar.png','モルモットの車「モルカー」の日常を描いたストップモーションアニメであり、作中には羊毛フェルトで作られたモルカーやジオラマ用の人形が登場するほか、人間の俳優が登場する場面もある。','2021','コメディ','シンエイ動画、ジャパングリーンハーツ\r'),(14,'ポプテピピック','popteamepic.jpg','作風は主に時事ネタや、ブラックユーモア、風刺ギャグ、ナンセンス、スラップスティック、1980年代後半以降のアニメやゲーム、ドラマなどを元ネタとするパロディが特徴。また、「クソ漫画」であることをたびたび自称しており、オチがなかったり、コマのコピーアンドペーストを繰り返したり、第四の壁を破ったりと、本来漫画ではタブーとされているようなことも頻繁に描かれる。','2018','ギャグ シュール','神風動画 キングレコード\r'),(15,'妖怪ウォッチ','youkaiwatch.jpg','原作ゲームとリンクしながらも、アニメでは主に小学生の普遍的な日常を舞台としたコメディ色が濃厚なギャグアニメとなっている。','2014','ギャグ ファンタジー','テレビ東京、電通、OLM\r'),(16,'カイトアンサ','kaitoansa.jpg','危機に直面した立川の街を救うため、阿園魁斗と有進杏茶はQフォーマーへと変身する任務を与えられる。そして16臣封の出題する16の謎を時間内に解くことになった。','2017','パズル','天狗工房\r'),(17,'ヴァンガードGZ','vangardgz.jpg','全てを滅ぼす「破壊の竜神 ギーゼ」の復活を目論み地球への侵攻を開始した「使徒」を名乗るディフライダーたちと地球のヴァンガードファイターの戦いを描く、ヴァンガードGシリーズ最終作。','2017','カードゲーム','ブリッジ\r'),(18,'AKIBA\'S TRIP','akibastrip.jpg','秋葉原を舞台に、吸血鬼・カゲヤシ（陰妖子）とヒトとの戦いに巻き込まれた青年を描いたアクションアドベンチャー。','2017','バトル','GONZO\r'),(19,'アキンド星のリトル・ペソ','akindolittlepeso.jpg','LINEゲームおよび2017年4月から6月まで放送された5分枠のショートアニメ。','2017','ショートアニメ','\"ファンワークス'),(20,'ガーリッシュナンバー','garlishnumber.jpg','女子大生・烏丸千歳は「つまんない事なんてしたくない」という思いから声優養成所の門を叩き、これを卒業して晴れて声優デビューを果たす。しかし彼女に回ってくるのは名前も無いような端役ばかり。「この業界はおかしい」と言って憚（はばか）らない千歳は声優として成功出来るのか。','2016','\"声優',' 青春\"'),(21,'イケメン戦国◆時をかける恋','ikemensengoku.jpg','3Dモデルキャラクタ―となった戦国武将の日常を描くコメディとなる[5]。なおエンドカードの5秒間だけ、日替わり登場人物1名のワンショットで原作同様の頭身となる。','2017','\"戦国',' 恋愛\"'),(22,'終物語','owarimonogatari.jpg','西尾維新による青春怪異小説。再び阿良々木暦に焦点が当てられ、シリーズの総決算となる。','\"2015',' 2017\"','青春怪異小説'),(23,'俺たちゃ妖怪人間','oretatyayoukainingen.jpg','「歌魔羅町かまらちょう」なる歓楽街に棲み付いた3人の妖怪人間が、いろいろと苦労しながら生きる様を描く。','2018','妖怪','ADK\r'),(24,'おそ松さん','osomatsusan.jpg','松野家の六つ子、おそ松、カラ松、チョロ松、一松、十四松、トド松は20歳を過ぎても定職につかず、親の脛をかじるいわゆるニート。仕事にも女性にも縁がない個性的な6人は、時に足の引っ張り合いをしながらも、ひとつ屋根の下で暮らし、それぞれの趣味にいそしむ日々。そんな彼達に、うさんくさい男イヤミ、おでん屋のチビ太、六つ子のアイドル的存在トト子、いつもパンツ一丁のおじさんデカパン、大きな口の中年男ダヨーン、あどけない少年（に見えるが実は成人）ハタ坊などの面々が加わり毎回騒動が巻き起こる。','2015','\"ギャグ',' ブラックコメディ\"'),(25,'お酒は夫婦になってから','osakehafuufuni.jpg','PR会社「スピリッツコム」で働く水沢千里は無口ながらも、主任職を任されるほど有能かつ努力家で、周囲からも尊敬されていた。だが、アルコール類は一切嗜まない。一方で、彼女は愛する夫・壮良の前だけでは彼の手作りカクテルを呑み、仕事の時とは全く違った素のキャラクターをさらけ出すのだった。','2017','コメディ','Creators in Pack\r'),(26,'エロマンガ先生','eromangasensei.jpg','eromangasensei.jpg','2017','\"ホームドラマ',' ラブコメ\"'),(27,'EVEL OR.LIVE','evilorlive.jpg','『EVIL OR LIVE』（中: 理想禁区）は、李暁楠による漫画。中国の『テンセント漫画』（テンセント）にて連載されている。','2017','学園','絵梦\r'),(28,'うらら迷路帖','urarameirotyou.jpg','女性の占い師「うらら」が治める町「迷路町」。そこへ五殿山からやってきた野生児「千矢」は道中で同じうららを志す「紺」「小梅」「ノノ」、師である「ニナ」らと出会う。千矢の目的は名前も知らない母を探し出すことで育ての親である「セツ」から千矢の母が迷路町にいると言われたと言う。人としての常識も欠けている彼女は壁にぶつかりながらも人として、うららとして仲間と共に成長していく。仲間たちと鍛錬の日々を過ごす中、「白無垢祭」の最中に千矢は黒い耳と赤い目を持つ謎の生物・くろうと出会う','2017','占い','J.C.STAFF\r'),(29,'有頂天家族','utyoutenkazoku2.jpg','千年の都・京都。ここでは古来より、人に化けた狸と天狗が、人間社会に紛れて暮らしていた。糺ノ森に住む狸の名門・下鴨家の父であり、狸界の頭領「偽右衛門」でもあった総一郎は、ある年の瀬に人間達に狸鍋にされ、帰らぬ狸となってしまった。','2017','群像劇','P.A.WORKS\r'),(30,'Wake Up Girls!','wakeupgirlsanother.jpg','「アイドルの祭典」で優勝し、全国的に認知度が高まったWUGだが、日本中にアイドルひしめき合う時代、いまだグリーン・リ－ブスエンタテインメントは小規模芸能プロに留まり、WUGもまた東北を中心とした「ご当地アイドル」の域を出るまでには至っていない。','2017','アイドル','ミルパンセ');
/*!40000 ALTER TABLE `anime_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likeunlike`
--

DROP TABLE IF EXISTS `likeunlike`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `likeunlike` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `anime_id` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likeunlike`
--

LOCK TABLES `likeunlike` WRITE;
/*!40000 ALTER TABLE `likeunlike` DISABLE KEYS */;
INSERT INTO `likeunlike` VALUES (1,1,1,0,'2021-03-19 22:48:57','2021-03-19 22:49:36'),(2,1,2,2,'2021-03-19 22:48:57','2021-03-19 22:49:36'),(3,1,3,1,'2021-03-19 22:48:57','2021-03-19 22:49:36'),(4,2,2,1,'2021-03-19 22:48:57','2021-03-19 22:49:36'),(5,2,1,1,'2021-03-19 22:48:57','2021-03-19 22:49:36');
/*!40000 ALTER TABLE `likeunlike` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recommended`
--

DROP TABLE IF EXISTS `recommended`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recommended` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `anime_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recommended`
--

LOCK TABLES `recommended` WRITE;
/*!40000 ALTER TABLE `recommended` DISABLE KEYS */;
INSERT INTO `recommended` VALUES (1,1,3,'2021-03-20 16:36:02','2021-03-20 16:36:02'),(2,1,2,'2021-03-20 16:36:16','2021-03-20 16:36:16'),(3,1,5,'2021-03-20 16:36:22','2021-03-20 16:36:22'),(4,2,2,'2021-03-20 16:36:25','2021-03-20 16:36:25'),(5,2,7,'2021-03-20 16:36:29','2021-03-20 16:36:29');
/*!40000 ALTER TABLE `recommended` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `session_id` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-09-25 22:11:33
