import unittest
from common import ANNOTATIONSCOREDUPLES, DATASPLITS
from hashlib import sha256
import pandas as pd
import io
from joint_parser import parseAnnotationAndScore

hashes = {
    "bps-01-op002-no1-1": (
        "1fcd912abbf85b4fd9feceee3d792a2d1a1742f439c361ee186e5c4eeaaae825",
        "d488cf3a6f4517d500d813017a2a8262d5bbf3436c2d08558273a972fc0bbd97",
    ),
    "bps-02-op002-no2-1": (
        "1534a76e44996bdee5880e958a300e636c2d6f5b9b6bb14dc6a6f9e9b2c1e6e1",
        "6718a9b7010783d1f28726fa3eab5e8f1c956e312a01daf50dad6984da1f1cb3",
    ),
    "bps-03-op002-no3-1": (
        "0ff0617882ac6ad4f5cda49caacc14c2014e8cbdfc3cc6d4ac3f82498f28c704",
        "7c55a85623408ee8c56dcdab998d8ad43b6badf0f9651766342bc9199a0c606d",
    ),
    "bps-04-op007-1": (
        "78c43470dfaf54e5ac710d2291ae63d712a34d621952f6aac6e8ed6306cf1d86",
        "d4aed0a1bf127adee66d3c2689a9a18e6a9a05678bc3299e3b97d380f70e01c5",
    ),
    "bps-05-op010-no1-1": (
        "68dd44f840e8582f2d1874e27150568dd71f89070512d11b8fd965c530d9004a",
        "d91d0d01f742df7396d8795118d30de4e69d132a1298809c40266f55dac4caca",
    ),
    "bps-06-op010-no2-1": (
        "3d242eea06e17a6750cdd6d894ab71207590c5829602db0a5858c8c1bd2f70cc",
        "d4d6b7345a9a80ddc0ca20fa41cfd816442f0a0e1cb05929bbf0b0a4a847e8a4",
    ),
    "bps-07-op010-no3-1": (
        "0ac9d70858b728ca11645db9d79ef01184875de2ef4c6595a1313791d2b5e3a6",
        "d770b743d1fa88ce999af8c0370e5ed191d0c04ffe24635d3978a88dbb042415",
    ),
    "bps-08-op013-pathetique-1": (
        "ad095fd08bd2dc25551858a6ff116ac254529421c51570f0e7a7ac417b5562db",
        "a11b914b48d7e3e02f4329726075d2fc8ae7bc3f3f136c7cda49684526fac2c5",
    ),
    "bps-09-op014-no1-1": (
        "92d14cfabf1c72f9275b1f9f8392ffa8b6eb750fb0068c25161eb390dcebe205",
        "54e206315dcac94ebb59423446461c7564471c655674acd9e1d8a08b3c81295b",
    ),
    "bps-10-op014-no2-1": (
        "da0c11b5763ecca3339b8eeb744abf7281a0bbf0c74e63c852a8df2191f7b425",
        "bb3e8a03b6138d5aa0343bfa16a67222b2e07178083d6bbf6046f247e3d3b7e2",
    ),
    "bps-11-op022-1": (
        "684a8426fedfc96c470f279256dc0d9e9e4a5f018c5b19b4fa5b98f5952ce9cf",
        "b3cc2e8af7b90001b0b9a146422dcd558cfa20410a59fcab3cda85b56dd1790d",
    ),
    "bps-12-op026-1": (
        "a5a8d2fb38b8e7df1920da9df54995a3d3395eb4428d702e011cd981bd0cb44d",
        "9c914814662d4bff3589d910279447826c1355beaf646365b96d82b5aba2f2e7",
    ),
    "bps-13-op027-no1-1": (
        "d4b106e75816be18054831621383d8c8733b66d090cfacaa54f544d5189fc68a",
        "874a5b60333ad0bac79f3b5bfa412914b695b62881bd1dcb6d316500f6ff9b8d",
    ),
    "bps-14-op027-no2-moonlight-1": (
        "36c17ce1f9091c93b2c6786fdc5136a217380483d4ff45803087857ea11dfc34",
        "978204b989919ff0aa523d0eee194f3974972c818ce0469efdebfb80349c3182",
    ),
    "bps-15-op028-pastorale-1": (
        "fdec56a8cf71a45ebce5fdad34a893b387bfdf86bca640661c5549ef955b0044",
        "e36e117c59741acc0a3ebba4a2e7a041130e274fdc6a7b6cca232b5ad562e6aa",
    ),
    "bps-16-op031-no1-1": (
        "42a9731fe94abdfa4e136fc0bf3938ddf5385f7db8fddde6c1fe1cb120ff46d6",
        "d7ec5c3ce28abad28df5859d31d00f8a4cc43556ef255450d1e8de6b931f2d4c",
    ),
    "bps-17-op031-no2-1": (
        "4e3d150609d750bb909c4012a043fe3f73c6d69c9cde18a04672c27bc59d30e1",
        "c553f4748661b1e2015a99ee81ad8b1f85c006a94ec8201e0845932fa12689fe",
    ),
    "bps-18-op031-no3-1": (
        "99b314c2086286b90102908c3881d26b6d402205750448bcf58c01e5da190334",
        "910daa516f03fc3df8d220523f99d7ce276903d1126358e55d32e45eea171990",
    ),
    "bps-19-op049-no1-1": (
        "d12c2eb8d7470b1c703c019c69e055ddf684e2aed9a461a870b3bb7b4b7c429c",
        "97d71b4a1af4fe447de675cb98318fff2beaa43cbc99c09455e441ccb8cbb8c7",
    ),
    "bps-20-op049-no2-1": (
        "724e63dbf82525e3527f3a1391154718b6ad28ecbb40bc63816b4fa0a7d2ed36",
        "36ea903be2b92ddb74cc29b58519c800daae1f678680572331ee4c6debbf8e1e",
    ),
    "bps-21-op053-1": (
        "71f2b30ff0f485f567f0e1eb1d0480f45a572cd10e480ce86b4a535f1eb100a5",
        "64e0fe04060473f39389524e44a9705e2a986ab99178e9e40922546ba39fe431",
    ),
    "bps-22-op054-1": (
        "27033e655e4099e98764d33b5a03e05489939d92945a102d14dfb47466650dc5",
        "44268a8c2a5ed441b9b0ccf3f3f533bfcd69b79b9ec27df6173dc3fb596d2b93",
    ),
    "bps-23-op057-appassionata-1": (
        "a4d15191cf93106bf97c2a32409e95d12d155dd0cb8e584caebf853615738bd2",
        "bc909133daaf9b2b292898f4a2aee7ff328470423fa4064186c3022dd1ce2c39",
    ),
    "bps-24-op078-1": (
        "94051e0ba68508be6197b1062a8e970753d8246e5b871e8299ef7dee839eaa43",
        "467c6f48bbb0ae22d62d1fc7cc6e7241865429068bd5949e019f9c1f9932252e",
    ),
    "bps-25-op079-sonatina-1": (
        "8be58b0b994131f05b9e33e2cb76250036d0ba31c88c434588b5e2d82f7bb4a5",
        "2e20af1f2aa9d284baa28025bc707e2127db027f7b7107f3e11fab738e0c0ea5",
    ),
    "bps-26-op081a-les-adieux-1": (
        "fc80107ab9a15daf90e26037ce62447ad004fbfb10ced4db0ae47c3bc1523352",
        "eaeb519578faabf7575a06733e14c095632f2cc07a6c93a11ffab46db527dbb1",
    ),
    "bps-27-op090-1": (
        "b516cd3dce80bf83073bfd6a3ad07328c5a9be85189fa5adc4a90ec758164bf2",
        "fe267d1a6e97ef55745ed54e208babae1ccf3900c7c892d0dc720c8394f0af14",
    ),
    "bps-28-op101-1": (
        "c3402d8a701cbcd877fec45faadfaef396d01292af08da7f9916c30bfbb6cafc",
        "d8d8952ded6f26f6c44250472e21babb1c8f97c09c5cd9424c3ad6a7d566698b",
    ),
    "bps-29-op106-hammerklavier-1": (
        "13798f76b2f92968696f494ed6a2483bb44f4895cc1ba906fc14828980dc373c",
        "f973e4bbc4ed0d2071282ba88c6f9dd13be3001702bcce044401d268b2d57eb0",
    ),
    "bps-30-op109-1": (
        "0c3a1a6b5b80ca2e2c758a77d57713165d2ea2aec8a99ae96a5dda84f9f5e6c2",
        "404411df509018aa3a7c90da9af686308f63ebe1f65078738b5de28e0c895d1f",
    ),
    "bps-31-op110-1": (
        "a3fcfd17e59aa7e3136dcfe3723875bb73cc2a46b709175872f64b67d77e8782",
        "85a8e0bb76a3387913094d7a97fcea451db2bfe5873374e87751c1bb268f10e2",
    ),
    "bps-32-op111-1": (
        "7adf65c5045650537d253fc11bb2266d1a87b0b0f3cfeeecaaa3405ca2e9cea8",
        "7ea164addd7002df8efb18e01d5a76f0fd3c760a2daa419d566c728dbdee21a8",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-1-4-mayenlied": (
        "7d65c5aa82e33bb466778c6643f92fed5ddcead53d49414f86943743aedf3f4b",
        "e54fdc61bcefeb0749555962829e9557351d2a3c245e6bcfa3a0cf42c808563d",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-1-1-schwanenlied": (
        "c76821fe5bce51404550a8ca7f49005a076effc32944c454ddeda64544d20f11",
        "b67c114383317c25c567711995fea132f647ee6bef01ec363845bef292fb73df",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-1-6-gondellied": (
        "6c78a053414e20098e59d2d68804f1f400bd295798eb7000420f8fcdd1ba7b78",
        "400caf2545025f30f163da4ae6732d25396d84f596dac1d06c1dfd39127f8f96",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-1-5-morgenstandchen": (
        "3f5a1aaa56625e296c9526467506f8d144761a973b5b3c0db2135232506cefcd",
        "cf2670796b4b138831bc7424826c15325ef92fc2559903a5ccf9284c7aed2cd5",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-1-3-warum-sind-denn-die-rosen-so-blass": (
        "72334d24fea81fe483094ac9795f951ae6284fa9250c1d68d23bb092bec14e3d",
        "18d857b9b12d02f7c173e295cad674f86005459024fa2e0208720bc10e796b4e",
    ),
    "wir-openscore-liedercorpus-hensel-3-lieder-1-sehnsucht": (
        "0179e77a38bf5fa1c8045e9b63906dc464e1af40dc179c75784e7cd5f0ff5e3e",
        "6bc405fbdc98666b83d3c4a09a82022a80b6ee5d1cbb5687a4ce8bc48fb64e65",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-9-2-ferne": (
        "d61e8e943a241ba1cd7df350eeb49594ce266714146c8b63f3a0125b19ceb0bc",
        "02a1932d0a7020eba7e2bb5703ef8ffaeae4da2f2fe3bf8a29254115621f5a24",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-9-4-die-fruhen-graber": (
        "906581dc1bc133285c626e7608da4889fbc39d866a7df9d683854e3413622030",
        "5001f824231aa965708fd29d27600dfeeeb6cf1c9e69cef027c6db3f0b5b1943",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-9-1-die-ersehnte": (
        "378cdeb0ce40b24f0ded391991e4774175d31b476c0eaf8563bf628c6872e932",
        "2d2f3c47a78c511c5a084e8164fb3c69759838e92eee31d64b2cca990674005e",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-9-3-der-rosenkranz": (
        "6dd3b4cd0dc06a54cdd246f3a24e2d0b986f09b2ca75c10a1540a5e4c1eb4e1a",
        "8bdaa4cce25541117cdef4727198899ce3e552034110dadff10508bbf26b1b40",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-9-5-der-maiabend": (
        "431b2b52b78475dbad571722df6f13853d0ecb5c332667dcf4f6460b0f058010",
        "ceb893bfecd0a49906e298a014947d9c885011e29e87093b5f7f703702858d19",
    ),
    "wir-openscore-liedercorpus-hensel-5-lieder-op-10-4-im-herbste": (
        "b9a797e6756b82d4e9ebb7c2ef265f5a482fa75b206c5491ad4142beab192e62",
        "75b60cec40810f703baeb625a40fba6c33dea8a3651ef55e35bae09c16b59ff5",
    ),
    "wir-openscore-liedercorpus-hensel-5-lieder-op-10-3-abendbild": (
        "7fc59e4ea3509db7a6359485f1aaff3658cd4b1b2a4c9dfcfbfd23acb64c12b5",
        "b51d99e460c4be7ff4991abae6225896120cd8e652c362e96bc7df4db5153198",
    ),
    "wir-openscore-liedercorpus-hensel-5-lieder-op-10-2-vorwurf": (
        "cfafbb03a0ac9800f702d4da047a83b190ce6f8a8f94a28b0a0acb9c68fa1824",
        "1c076cf3941345d54ea23ac0f9a0b56118a97641b289752b4e452ff1253073c7",
    ),
    "wir-openscore-liedercorpus-hensel-5-lieder-op-10-5-bergeslust": (
        "ffb269f1d96260a188955f07fb02f4749b939baeec09104b5e265a590bb5f7f2",
        "333a4099023ea961bde3a066c8f168611ed36e1e46ce18a53249a297169794a7",
    ),
    "wir-openscore-liedercorpus-hensel-5-lieder-op-10-1-nach-suden": (
        "cca46e3d0409b01260742c052fe1fb37dede490fc69b640dc41ae602cdb7f199",
        "1015b4e31261ce90d820046beef5bccd3383fb3c879e7ad8841dba57bb2fa5ec",
    ),
    "wir-openscore-liedercorpus-schumann-6-lieder-op-13-6-die-stille-lotosblume": (
        "5a34822341670d471a493469311986aa5271ca5d009e6b8b957b0ef27b31720c",
        "a6b19184401ed272c1318ce583545b5b58069f00f5ad6b654a4fcdee88ee2430",
    ),
    "wir-openscore-liedercorpus-schumann-6-lieder-op-13-1-ich-stand-in-dunklen-traumen": (
        "bbabbe1073a98c3aae60f601e6d472fb002db160dea3a92b5f3a6f56b4c65547",
        "483c81657c5acbecab9ef089d982e1b2f767d4154b9b6b2029d14f7eb42f4b48",
    ),
    "wir-openscore-liedercorpus-schumann-6-lieder-op-13-3-liebeszauber": (
        "683bc9145f3be046f3d37b06517ce96dfd8186e8ccb04147d11c259fb0a96090",
        "8d4a3bad2fbce73ed217ba7d662a92179f5ab6e9fd979d70cb1c5600b5ddfa08",
    ),
    "wir-openscore-liedercorpus-schumann-6-lieder-op-13-2-sie-liebten-sich-beide": (
        "e3ecc2c589b368373b4c85b40309ac86190e8ac86f0e7695bd9b71163910a3d2",
        "1200f147efe5b7bba7168ff313b0291fc03a090dc237f29e41e0628b2b44a0d4",
    ),
    "wir-openscore-liedercorpus-schumann-lieder-op-12-04-liebst-du-um-schonheit": (
        "8805cf640f91b385f20f2fe2033dcfe5df0a34ca4d121793613227a006a25637",
        "7e4b4727081c2fde6a9226ff483124fbeb50dcc0ab9d90ba3825cf1fda46b0cb",
    ),
    "wir-openscore-liedercorpus-schumann-die-gute-nacht": (
        "3375f8b174af8ba7bc8488c58011c11c5d1321c95b7a40fcdccb08945d1a6168",
        "bf1c254248b72c7af630f16197d481933ddd1bc83f8aa8d0ae2db48a26e596ee",
    ),
    "wir-openscore-liedercorpus-coleridge-taylor-oh-the-summer": (
        "9f7c3357a464e532b6b74e00def9e7d8a9a6efac8893cd34a2dfd5fd4c45141c",
        "7415ebcfba7c414de1e63afee20b92578028eedf9fa8b6faaaf23b8bf1ff522a",
    ),
    "wir-openscore-liedercorpus-franz-6-gesange-op-14-5-liebesfruhling": (
        "484ba31d36f80fd6f511d85bd2e2b14aa026d2bfc5cbc0470bc2b015347c6f3a",
        "d7dd1bb83140008315530f43ba4db9e7cc772d024d0cffb07110e035d5337077",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-08-nachtzauber": (
        "aeeb00bbdd1991f2b6a04e371a772ed4826586e7306869bd36ca7a2b774f316a",
        "19a2fe3f5532635ebb8fe01b7af3b8c48d7a0a45e915519b45fa2748e7a0efa0",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-19-die-nacht": (
        "16706127ef8d3822905b950819d1732bad5ea71f94dbfc32c3eb0090de9184a9",
        "634d6b06d4d42d5181851b16dfecaa99deefaf9353de57de8903c4f7ef6a87f6",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-13-der-scholar": (
        "7262303093101d92c1cce5cc712ffa262c1b11aad94f932d0ee4943e993f1ef9",
        "d088b13f785561d3b454907a6c67fa9a427730dd1b0451db9ef16df42ef227fd",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-14-der-verzweifelte-liebhaber": (
        "72349d81eff9cdae78e2eea848b8224ec78c0e9d84443b3e281a949a30c03c34",
        "0f3ffdde9451d1f0992083269dc731d1879a4f400bb7ac99535422b00a56bece",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-20-waldmadchen": (
        "c2bb86aae3d4e8868cce6b00602c3a366044a639476dd85c9bb1406719a9db75",
        "a10ba07fedc17b3fca930543eecb8dc58fc2d085d4eef64d98ebe89a7886f150",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-04-das-standchen": (
        "7bf4349c42f364ff3658748bf69476d9c999c40c8e097c09449b9c7d716ab80e",
        "18829a6dab402532cbe0cd8229c744a4eac2b73c5d8397e00ad53a4b8b71f5d0",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-15-unfall": (
        "8b22123c393bf9d6edd5460c22e1547144b51161e30665314962d0050276f754",
        "bda6f0e4da5413ac5a87b33afcc242eb78e50175aaf6c54ad5b63557d704d332",
    ),
    "wir-openscore-liedercorpus-chausson-7-melodies-op-2-7-le-colibri": (
        "96daf9ce872d98529623be27833c0c2cf9b51b92ce4a848a8fa675326f09aa61",
        "1fad9d06edf3c78ff30e37403e615a7d2d1a10911040bdc1757bcf26e35304a8",
    ),
    "wir-openscore-liedercorpus-lang-6-lieder-op-25-4-lied-immer-sich-rein-kindlich-erfreun": (
        "ad74214f89ea960999fdfeeb7997097e0f63f3818bdca7cd2b0925e755b7e765",
        "568bebcd70146748b13c97699e9f5a5fa4355b4022f27837f501fd262d6cac42",
    ),
    "wir-openscore-liedercorpus-mahler-kindertotenlieder-4-oft-denk-ich-sie-sind-nur-ausgegangen": (
        "58a8bbcdf0c7787ce98c7506fee21a04763703c2e9561a3abedab5a5b293640e",
        "c3ce03ef6340bba750ddf45f27c1d9b91bd941a50e9bd6847a2132001387c7c7",
    ),
    "wir-openscore-liedercorpus-mahler-kindertotenlieder-2-nun-seh-ich-wohl-warum-so-dunkle-flammen": (
        "b0aef257d7bd64c5731b7b2f570ee51d7c4476ad7692763fc7335beaf350b8f0",
        "231e6c1d822cdf2df61aa4d6cb846a69867d522c29dcd04cce21323476af53cc",
    ),
    "wir-openscore-liedercorpus-schumann-frauenliebe-und-leben-op-42-3-ich-kanns-nicht-fassen": (
        "b7159fb23e3679dc6f9bc75678bbb94961e054fdc7d8669290a3aa944b2794c6",
        "a33cea8c1faa665d3c57caaf8c5ed43cc3d5bfb2dbd54e50d205a664ea986746",
    ),
    "wir-openscore-liedercorpus-schumann-frauenliebe-und-leben-op-42-1-seit-ich-ihn-gesehen": (
        "e0834e669f5f8e843f425542f3a0f46909e12390b1c33f427fe4e1e939025fb7",
        "fe2e208c88236f6468c7b67ceba82ff6747594789057900af27b74ac652ada00",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-04-wenn-ich-in-deine-augen-seh": (
        "0c1837296a045d26fcf6326b42ae9c8cf445d2b9a1b4fd7c55f4bb5da7349e1e",
        "0b177aac01ca8c968634bb75b3f93c8a21c1133b0fd8af3e63858e8eedfa7173",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-05-ich-will-meine-seele-tauchen": (
        "98aad3330706ddb04a06f50050d1b9d86a9e4df6112a38e721245cbe848b6407",
        "40992f52a2aea71442d729b63c426c22001b43d5066d7362985d95e6dda99511",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-16-die-alten-bosen-lieder": (
        "ed9043658f8a9bc59a558268ae231284a18b06e0a67c475eb2987bb27f011074",
        "b4e0c5f02adf75f9d17356a6ebda6bdffe1d181d2f979de834b4875c8fb8b402",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-13-ich-hab-im-traum-geweinet": (
        "ee267ef47b067108540bf1a787375fb02ed678249531f0880e1680e39270182b",
        "ab806496a6d886980022c52bb15c498644f1f6e513cb30b25e1f8bf9494c458d",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-11-ein-jungling-liebt-ein-madchen": (
        "6b3b710b9649a9b97104052b004ff46ab90f2811bf44128e5dc70e7f3ef1199c",
        "c5f02631f6026ec4f326922d24b0b95260fa64004743631704f27c2081c2c635",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-07-ich-grolle-nicht": (
        "258518c0dc01b6ee3f09a449364b97568a92f15c968774817066ba02ec04a6ab",
        "e0848c932aac59bee08ff71b1f42ef2561775f5eb0d263e672a8a916d37b0cdb",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-02-aus-meinen-tranen-spriessen": (
        "b29319728e487a67e24f7936a7b184af8e306654f61c032b9a45838adf0a8551",
        "81feb25f17d47775cbbcd34d4eaa72b63a3fbba3464dcf0d94be715942c01097",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-09-das-ist-ein-floten-und-geigen": (
        "1c89d6f705b728d3d57fe2427ba92d0fdac9f538400b076967cbf0bbacbeea9f",
        "f0f70431dd0a56e9bdd5944fa8622a75b9c1c48ee457a2ad3f15ad153a70478c",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-01-im-wunderschonen-monat-mai": (
        "3f3b36f042963fb5f24083834e98d0ffc1fd41f06e47167a32fe0bb0105fb57b",
        "5d42551fcea90e82492bef9fb9643d2cf7830e68adab6dcce93f3f94046635b1",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-10-hor-ich-das-liedchen-klingen": (
        "97f96552a74de92216a1e1072074d8935ce02538e2bab172cff1ee6a39565b32",
        "93d38dbe0c99339703bf04790ef79fc3f0cd9708d8d1470f60c1b3028ca30602",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-03-die-rose-die-lilie": (
        "cb3f847f07deecc77bb9e8e40b9df1b24acca50222af43143bb2d66b8eece551",
        "2a547a51ce204985d9b198d33e78126c30b18fc5a8f03fce9e2b9e41449e545a",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-12-am-leuchtenden-sommermorgen": (
        "6f16dc1ca5fe0640249d696f6d5787b3622f884516610d230eea16264ff341bb",
        "f496322caaa260b0cb62c30fdf7c6d1eff99ed17c604e9ad743a20204d2461c4",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-06-im-rhein-im-heiligen-strome": (
        "7166ac9475fea206df9da86572a7c51ae21705634b612b19c295e5742785b618",
        "14ac63e49f5c8b5718cb32776eecdf997e87d4adaff9494ed30f60e189651d56",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-08-und-wusstens-die-blumen": (
        "c586306e4cb62ec379ba6fd6028f19534867f5e81b2da6074705754fe7ccc9fc",
        "86ee60c7b379a291a0e16630eb4b371fafef5d4d5f72929d8ca294d0cbd19f24",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-15-aus-alten-marchen-winkt-es": (
        "3cf1441d5a83fb9209a033091e12097dfde14d7b1e1b912d1a8a24c759e707ab",
        "65a53dfd934282a10cb5b53b952d421f771251b69f931694f71f4564d256c4f8",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-14-allnachtlich-im-traume": (
        "23ea1a308c283a40d479379db6b3e38f7ca9f6ab123118080d1b8ce3db93e575",
        "535ac32d43b2c842b8603ec02e68bac9460d28dab9f21c990332e2e53647d178",
    ),
    "wir-openscore-liedercorpus-jaell-4-melodies-1-a-toi": (
        "82cf2f4f8e111fc3e96a033ba8e3b566fe0978d5aa5918ead2951dd0a0b2c9c4",
        "63548aaa57c8f73e7637590dcce5a5cf9c76ff12e87d466ab108951d8557e719",
    ),
    "wir-openscore-liedercorpus-chaminade-amoroso": (
        "79410593374ea96611bded5e5928f43d4a92574594f98ea8106d157438e87408",
        "008214ec7581228c84636a09ed646e25e72bafa1e4e08cad3c5ebeaaa2cbca0f",
    ),
    "wir-openscore-liedercorpus-holmes-les-heures-4-lheure-dazur": (
        "806e3d0a68990676e94ec5e242ae2bdc4b0d885b21870df8360a0c36d5cc9e44",
        "f9199ee4d33d2ae1bd7c4bb4625e17c2d9040017a0e3d8fdc4fcabf41cbe02fc",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-04-wachtelwacht": (
        "70c56c6a1a9370ed458e0e1ac350a31a232a82a9a6bec7edd1ffbade9f5cb4e5",
        "2695e6c9a91b9df3dffcec0348b29bc002f33995aee9534acd4ea32ff861b795",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-03-die-blume-der-blumen": (
        "118a1374c928e17d5bf27002ce3c1a22f8298570446170ee4ed9ef3fecc61655",
        "4b031c08118fffba0a9c338f93228571747177f9e7dab2598a1c88f43317327c",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-02-der-traurige-wanderer": (
        "8c375a7e43a7f2a08152a4d1447a5ee09660150f03485d58277e95907779b416",
        "ecce10b61abd023e8b9aff1b95bca190a27a28784edf17dec4ddd43651535a2d",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-05-betteley-der-vogel": (
        "06f28fffeb59b93f7ab96b482929ec5da26a29f1bef0ebb2ed427f8a8b1812a9",
        "26095f933733a4e31498d8b24c45c4b3f3b8f360fc18ef1ba1938c55b61b777c",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-09-hier-liegt-ein-spielmann-begraben": (
        "82017e8df2622a546766945423f65216f4127065cd2e72c1b409d02a3432b408",
        "b419ec2b06c022c89ea55a24d44871e612c00621a26e2a3b8c5bcbc9ee780535",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-08-kaeuzlein": (
        "8d00f1306686d14f4dec7e18cdbd661b91445645db0429d571697dab7749fb7a",
        "66c4505e1f75a68127268ef983e7161493c0f2741e9eca6cd77be97d52148a14",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-07-die-wiese": (
        "ebe39bc6fd4d82f22a6281928fd1dacceffea40346ece11a873c421a1e432bf8",
        "60eefd70939eaab92be5d82ee733ec62e064da3f71cafd7f2d18841c821fe80b",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-01-fruhlingsblumen": (
        "8d4c3c1ba8ddccc328812f6b817d64b18186bfa0d7ec22be7fc7c3a9724e0595",
        "c59ae03a89cac3565e5389cf975a5816c07152f5a6e667ed2a8f19735831d7d6",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-deutsche-und-italianische-romantische-gesange-10-ida-aus-ariels-offenbarungen": (
        "0ccc6dd49e64704b7cb425fd4a4f579ab1c5de7d7d684c13bf3f91577019f75b",
        "1f57b34e2dab14ffe4c2cd7da1ea9f45a9d2deb1d13f85845d587f1500e15f50",
    ),
    "wir-openscore-liedercorpus-reichardt-sechs-lieder-von-novalis-op-4-5-noch-ein-bergmannslied": (
        "1f340b4562e1d9c99402664d81c544c665b20fde5e9a96ebd685aa0a7999b45b",
        "763366ce6654473acc8d34fb037474f4faffc264da464d6220a228258079fa48",
    ),
    "wir-openscore-liedercorpus-brahms-6-songs-op-3-3-liebe-und-fruhling-ii": (
        "6bcb6339d98a0bb5c4349f33e45fe8f4f053f2da13357a16f3ffe1f1ca3d8ca6",
        "4c0eb08dce746ad7f892d394fe54e5cd09390bdbacf0fdc985e6f0529abbfceb",
    ),
    "wir-openscore-liedercorpus-brahms-7-lieder-op-48-3-liebesklage-des-madchens": (
        "b1c861b8fd9685017b650dad2521f3ffa68cc078fddf06a8fd519b4455f739ee",
        "472af9e9a013e6d146140f8753db82c5766789a58e03294304fe5113581ab93d",
    ),
    "wir-openscore-liedercorpus-schubert-4-lieder-op-96-1-die-sterne-d-939": (
        "fd4b256605033d60029c43bf0d7cdcb245d9cd2d7b7c926b61f1b1e91636ff10",
        "2804609ec5fcb3d2701076202905c0aff76c2c3feaa6c966a56f33b9eac9bbc1",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-16-letzte-hoffnung": (
        "cbeb5b44122ed7b0bb73dc6b544a9926adc5a4ca91d076eff6fe2ddb89c550be",
        "398b4bb2ba05fc9e9ccdf9bce28785df6661eb29a65c209bff40d9fd2e554ce8",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-23-die-nebensonnen": (
        "ee2338eb5d94ca3d8f220fe0d543ea5dc45f81dc98120e356604d40fdf65b5a9",
        "8e590d418ada5100428ebc3399f04438366f2501f270069e6c38a22ad132af69",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-18-der-stuermische-morgen": (
        "32d1ce937536305328d711fcbc33d259877afa6f6a45de43f255b91807689d13",
        "4ede8ef8d6b86e4eca22f6278d191141bf817b160a12f3e7dc17c0a0de5a4b73",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-06-wasserfluth": (
        "57fedbd79e353fa56939d3ed345f2b3185a258b1eeeb08a5c82095dcfe0c7e8e",
        "1136a19f209946938b160fef604452ee83a580d2dcba9f8bc5892a63e5b2ac2d",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-09-irrlicht": (
        "cd976a44bb929d7dd208e6abbc34ac07326e15d90c28b0525d427f9ac3dc0e04",
        "d17c357f333444a5ec5d92bde89df0c137af8e4bea7c29f862f610b8ded766b3",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-04-erstarrung": (
        "1d2e0b1a2e65a229e2c93f34d8e8c72a57a499b68525d6cb7e2757a400914a98",
        "e07b4d9a2f396382aad07a86127f0aaadb27ddf363b0f79e99a72f9a4b3d0630",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-14-der-greise-kopf": (
        "bd627f246fe36abf3a8f4e01b719bb1e8e8607257d77c240669a9dda50961b86",
        "575917f3931bc4cde8c4beba52d782a1b9772b4d80074cc515e10765240207b1",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-20-der-wegweiser": (
        "dd1a928412447e60e9bb1f704778e6d5ccebbdafa8356bfd32d35dc3b14c4308",
        "a098b7c828b1d2432a72ed7839459c1caa03e05cc82bc14ff0bbfc2eb0e56bbc",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-01-gute-nacht": (
        "34136e586be969f09b48fcdc079a3ca1aa463485a00eba28df71d9b8ece38773",
        "eb7963edd08238d806a76ea647f819bf506116b63537a88da8fbf725624c86d9",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-12-einsamkeit-urspruengliche-fassung": (
        "4844d3d2da3c99545dcc14f0d91f04aec855698b953b1b8088c828aa94aa3026",
        "6d2aef45f850dadc568ef9f8d6e43e07e498caa376343e9959967b43556c7d18",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-13-die-post": (
        "db4e393416a6116e200a0f5285257af412457d991fdc567ac7ab1044e32e36b8",
        "c2110d7f13f8df1137ff167317162bd680bfb067d5aded1b149451cf4fa41c5d",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-03-gefrorne-thranen": (
        "19f5d172663065915ebb582059760cb6d7ffc6020f6a3b106e550c9ff1b02f21",
        "78f128d4ee1f3a61ed02feaa212f005c3223f590ef04ff3e1b2b91d6d5e3a7db",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-21-das-wirthshaus": (
        "95475054c383d7f35c9fb18a65e743fb52ced411caf9e89972eac3300d6b1f82",
        "ea5312b9ad9d949280f3d7b239cecc64cde4572cf04ed5e5ebda762b1a981f26",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-17-im-dorfe": (
        "d79b74ea8c215d7b5e3161ad8a99f9217ed82011d3f9bb2e543d75fd99432783",
        "ea0b37858c4cd0c6f33e9d9816e85e0476c0b515ec67302d0e92872fb607e76a",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-10-rast-spatere-fassung": (
        "69844fac4584b15a95dcba9298f95cc36457a292d878b39e184683d2413f8505",
        "28ce8259244a7101469dce72d10d5fc9f73ad4146edda47f3ae1b8e412056a15",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-05-der-lindenbaum": (
        "bcbb35224a90bed13ca44a79030b6ae8e18d7eae549eeff8e55e4a8b5d0443e4",
        "e7645cd78f7479992fffb8ea8b9b82769e36e39a09d86e3a918bb183b36ef963",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-11-fruhlingstraum": (
        "2f1212a9e54ee9204847ee4d1a80dc1943639d3a2f8dd9e4444be8d749f216a4",
        "bcb905422edb94cd8b2bb650e25985e6319e83d2962170c98ed6e9df6a2a401e",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-02-die-wetterfahne": (
        "23876161273b0f628fe666f88420a779290507349a2df59e39a4b6f48da75134",
        "e7f2d8b846142c4caafb6cf59b354f6e9e8214ea76f2daccee023010650330de",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-15-die-kraehe": (
        "9c912bb8e47409b9d13d1e53b53893119235061266256bb2aef7c0f1d537b738",
        "14a10a6647222941e9954bcaaa34e332d5e4bc2db8898f037394766fa617571e",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-24-der-leiermann-spatere-fassung": (
        "b1db672435619b367e4a541fb06c1953e971a74684cff7c20d25201ed61dabe5",
        "768314647d95b1fd5f2225cbbf9d8f1a61537c627943db9f5bc119c0f13ffec1",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-07-auf-dem-flusse": (
        "2464db3234a319c5f8e2c32fc9380fab9fe1bf255f9283fa41c3ff059691edf2",
        "3def580429717aa34c9e520604423dfb119d28f89e8ad1748d84b01b4065394b",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-22-muth": (
        "de812b109c5720bfcf44a345ffba5705afaa92767265ee25c9652722da50ab22",
        "558bca4edbce6e81e693936a100e7686cafdfa9b5c44178952234101a3089e71",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-08-ruckblick": (
        "d3c167b06b88a00178033e49952d65b7e998e6fd8137b61002193486d5a56735",
        "aa92e5c56fa2bcaf021723651f634aff00e67c0cebcd6dabda653c4ee64e091b",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-19-tauschung": (
        "ff01dfb74de3ed1546558d7587180b510dbe963a54d5f047bf44e2876cf4b9db",
        "9be6167c3e5ee3d7151e4c172b87d6adbff26a798e13c17658a42f84acf22497",
    ),
    "wir-openscore-liedercorpus-schubert-op-59-3-du-bist-die-ruh": (
        "369329f01e805a861cbdf938caf697b0a9e9a4d5a785ff6dc7205faeffef8737",
        "1d8ae554e7c632729a8851ddd6d778bab457326fdd4c54045060f2cf3f52f6b2",
    ),
    "wir-openscore-liedercorpus-schubert-die-schone-mullerin-d-795-12-pause": (
        "87d0baa381c4f7187d73fc7c2fbc977410ab798923c0f956029b2e2e6e98de08",
        "11ffde24da48cb9d515e2c9faec626d448adee70180c579d7e9eaa162a71cb0d",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-02-kriegers-ahnung": (
        "8ed7fad78b4d1bc4f23e35941ba79790b63c68005577d50df36a7071dc9c4da5",
        "7af082408a1f2bf1f51e0d13865254b8198c2e4bcbd6e0600776464d6fc8164a",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-06-in-der-ferne": (
        "74bbaadba546542e297c420a8d51a7711eae157ee88c38c8c8da38d96e63be2a",
        "72dc90ce45d9f751fc2cba82488f56b5de7030b9dbe8604ec4540d55760728f0",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-07-abschied": (
        "11c8ea39cdef8fd0d030a6ec4e26e84d28b2929365241db5d96704430f9706b4",
        "cc81d1321eeb58c29ad6943990d5943df5fb70873d700b03f93855d652a72fab",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-10-das-fischermadchen": (
        "ea8a37b5ef8eafdbbe4f54942d593980d43896058977d435a7eeb5282068ef6a",
        "f9bb8b6489ce7487755e901c97410c583c2a11abaa0337158131678aa8cbd073",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-11-die-stadt": (
        "84af14fe89a15668b0592afa18c25a3f704e854dddff912a405dcadfe5208456",
        "59ee1735170c78c77a1fe27f63de87f511635cf12ce8e552e47d8409b11a2cd2",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-05-aufenthalt": (
        "0691a9a7995318929926ac2383090b9e1bf1fef99e7e0e1847fc37215028c8e1",
        "66056177a77f93f701363dd1bfbad624876c337046df61d9882b247217ea51a3",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-13-der-doppelganger": (
        "79dd54704f6ebed585f2118d71ae7f8dbb63a22b8b737e06792e0d0a00aa3592",
        "0e2d2c3193c72681e169a00e127846f55caa20fd0e4dbde6ad322f891a6a102d",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-12-am-meer": (
        "402b72db359ea84cea3c68df0dd5548da1cab50144464cbf609ce5d424386ff7",
        "e0e7abea0f9d075b1f2ba803a0759580d0e7427dcb924e111a1cdc723498143c",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-14-die-taubenpost": (
        "03ff254020db70b175d7e1da98bcbe6a4c37dbeda2cff9cf0b5fec8d0ae34fdd",
        "54cdd2161b330c8b8da6e71d965a8c28df45b8607b6bf7a885c42344ca5ee3b2",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-09-ihr-bild": (
        "8909a8d72238c89a9c2017c0ec965f58388b5397cc9cdddba2fe03b709ea1dc9",
        "2afe4b80f4f480790c1dc35787947de94c47f4d881248e5be64e1a33969536e4",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-03-fruhlingssehnsucht": (
        "ee8a87bb2de581c3395d3948c048b5cd4706f9959d2ddc3b31eb9bd30e9e8d35",
        "e27c8b9d095970cc76c559bb2b00f2e4add3d7a4c8f7a369bdb884ae9993ec43",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-08-der-atlas": (
        "a4d845d01703e58f547c5eedf628975e5a65de5af8fdb15ab380e28b97a36d01",
        "f79c9ec11585a92a4f41d3f62a4cbab8571222dfeb71759d93b0c7331ba13c19",
    ),
    "wir-bach-wtc-i-24": (
        "089bfcc629fa8ec1be79595f4af0b89f0a0dabaf77c94d85917b6e8dd523a036",
        "8fb64fe411963a27de13caaef4b62af3c27dbba756394ed96edd1e9d6154219d",
    ),
    "wir-bach-wtc-i-15": (
        "7573780602ae5cdb088a2683e3318af42ac5afdea587717cab5060e7ec8ae8b8",
        "528ec9142b332ab231630ed0a293ba80b3b02f35b1517bb78daabbd880a0ae69",
    ),
    "wir-bach-wtc-i-8": (
        "974d84b36d9b0766689f30306cef84bc65b893e8e455249e6f816b216a9b1b48",
        "d927e102dcaedd7b26b48a8ee1a9f342d39fdaa0950baa409282a07dd2f2acf5",
    ),
    "wir-bach-wtc-i-3": (
        "9801a6db0589a52647915c328cb342615659e5a73850d99125a192229e0488f1",
        "b736479ee227f5e475c779a4009fb91d1c340e688855c9a42adf3f4f374fa7a1",
    ),
    "wir-bach-wtc-i-7": (
        "4b8023ff6f796d5c77c22f038072aa28a12ee0da0f18db45ced8eb107c96d0db",
        "a8e386216eb89a14ed73c94c6c1d0bee0903345e4478d6f3e71340df3c1598ac",
    ),
    "wir-bach-wtc-i-17": (
        "5f85d505bcc08bab97f9286380b3d0cc78e885dd2887010a9a1a52d4418c6f3c",
        "b6f2da42a3c58519b20ad1a60c553a16e2e87b56f4852edd65d6794f944004e4",
    ),
    "wir-bach-wtc-i-16": (
        "89224aeb6c7603f01491b6e092a7ef4595eaca372fc9f47afa998339f9c9ebb0",
        "e40a89fd3e861255d533e68092c9b1fc36109e7c4107fa0628b7700667c5e576",
    ),
    "wir-bach-wtc-i-11": (
        "10e8c572ea356fb37dcfb167e2fa1430f00a7bb253869bd2405f5ec43b7648e5",
        "31d8c498130cec13966cfb800d57916b58dbc547ff5c5972a013f2fe0d3df981",
    ),
    "wir-bach-wtc-i-20": (
        "b1c4d9fbbfb30cb3b357396b6c3570f8007b74c841e5595082007498d54829f0",
        "1a871d8cf5ef2ed50953fb4ea0e7acbf80ff29962f1ffeb445cf12288475de03",
    ),
    "wir-bach-wtc-i-19": (
        "09e674a673507f9a4668732c0ed31f2c42561b2ecde109e7ac5ac0f1312a93bf",
        "a9b989b0cceea6f2ccde4c26d4a84ee9401a74e10599ae03046418ebda14ccc3",
    ),
    "wir-bach-wtc-i-22": (
        "1e65290e5502017ca0042bf62a2429341bb9ee23a76dbb65a3ed6ab76638f29a",
        "0a1484babd7a9fbb0ab3630c4f6c7b2d7febb1adf192fd866236f30466b313f8",
    ),
    "wir-bach-wtc-i-9": (
        "859f0445d5a337912b9670661267a4ed95bde2cb0bec74f1ca89a7c1d08cf320",
        "d581caa7ff81c4b0b78dbf57de49b869ad414594963ef50e7e37c0699abd166b",
    ),
    "wir-bach-wtc-i-18": (
        "5fdd4c6ee8cd376f60d01d3457a831ff2eb4ae19bb12cc44297445efb462a25c",
        "fc5b861696722069884752d6b3f2e528ff463b9848a4e10f5173705e03fcd8ef",
    ),
    "wir-bach-wtc-i-1": (
        "e2c9b0e4ca444aefbfc6daf9507eaea31931ba630d25fcc97a3cd1bfd7194b37",
        "7179b0aa86707cc2e6db004c30c5b94713b1cb0d201a58d4d70197be6311f974",
    ),
    "wir-bach-wtc-i-5": (
        "daefb1862be3b76bc321a6a781c6c64582ca1754bbf816dcbb983b6b4509acf7",
        "a522bed78e8d045b803d65167271668defc5a106e6aaace9d7c354e46d316f53",
    ),
    "wir-bach-wtc-i-4": (
        "703dfd6f51f99799b759bd3fbefd941bf443e29583ae95a5ceab7ef4ecacca1a",
        "3a8471d25c3f71a71af2de19f351c95f945d3de4fb919b4c7ef92bc4149855a0",
    ),
    "wir-bach-wtc-i-6": (
        "65fe8f6970448e4f34b7278200872019295bb2f323d690ab879ab6c89d17b43b",
        "4de7ea61b6c90bc231923c926cf8a36ecd2b2aa2829c4d5bdb5e05f336e037f1",
    ),
    "wir-bach-wtc-i-10": (
        "ea97397e7bab4e54ee6b197e25e639b56d6841165c17212540a319dec40ee480",
        "a36f889320af6ac986cb4e3b091d4d7edc1662d4fa0bb2e15f7ec68fa7ce483a",
    ),
    "wir-bach-wtc-i-14": (
        "fd6afde377962fc12dcce570d80405b957d8c2ca049d39ebc6602e9b4279858f",
        "9db2438ae5f5c0ec5e5fa16baad917a3ed910285de1e3c804bdfbb20aed74150",
    ),
    "wir-bach-wtc-i-23": (
        "b04042a864e1f312fabf75a3efa51f64c53e118ea5b0788148a9e220a88fdcf2",
        "26162fa3884931608a838061bed1bb74be76fd7ec5822dee5292aa08692e043a",
    ),
    "wir-bach-wtc-i-2": (
        "3d6047c714bc6e98b6c2cf5c5e846d57992f6ca6e0065b2d1d33297117cc90df",
        "e13adf687ff1b80ff801c34aa72fc4ac66312c58663364c4ac5d3bfc9aa4dc11",
    ),
    "wir-bach-wtc-i-21": (
        "8a7aaafcd711ac82afa9892cdb4777c7dfc9934091a67fef4136bb670945eca3",
        "d19aeaca89172737c297dfacd8e64d1e76f34f73a6547631d5e48953f81528df",
    ),
    "wir-bach-wtc-i-12": (
        "a77a439f6df7b61cb2d5fb76838cec1d744ff711aadd57e8b79a853abc4ca2d4",
        "6cf694fcedb9cf1672568da5da04dc23258e72176b9991d1c1777ce0306c49be",
    ),
    "wir-bach-wtc-i-13": (
        "59831feaa2ae14174c35140f8a88c2ecaab5df2a35609b958457776eb0651b93",
        "9c2fae600646832ccf1fa93898630bd14848c2c4dcfe9fc08d5a097a3f8d955e",
    ),
    "wir-bach-chorales-1": (
        "085503d447c415afd0ea9e460519e739fcf688121df98346657d108c1ae1079e",
        "9676f11a2b26488bcf30db90c15576caa1ea2a616b909e376d44b8b804e9d138",
    ),
    "wir-bach-chorales-2": (
        "88c42971649608ccdb409ee9f3e7d867e627031bde02f195b629b32761c6ce76",
        "a017649b259ceda9c0ee8a74909893a69d01163c5f60ae5e631dc3d2ac58bcb5",
    ),
    "wir-bach-chorales-3": (
        "3ab4cdb20b37d35b7f4fbc5c70affbc979fa734c9961eccd6a59a2c9a891991b",
        "49553bbbfa8e79ddac3b35232608c9db07c3bf2582a161b805e6eec891e1fe8e",
    ),
    "wir-bach-chorales-4": (
        "6c82412c74e36147415562247ada1c1ef6befc57e05e5b739a8c7804fd990d1a",
        "5b9a0acc0010297e9f49f8c43d098361deb28f67dfc13f9f6b682cff9ec1003e",
    ),
    "wir-bach-chorales-5": (
        "ebf2d7e298f5fd1a46b0ad6f6f0ab0a85e4f1de752b05c49c202c051ed0ee5f4",
        "8fd35db74f930089746d03248b8267882c9508d8f005aec67e9f4e23d74c27e4",
    ),
    "wir-bach-chorales-6": (
        "6947a928c259e3899ebcd450a984b52323d3f513d42f779b3045d097317f192f",
        "3946fb6c7dc6a0fe772f88aaefa5d32f9b42f9fcc476e9a3070f9e5b33ea760a",
    ),
    "wir-bach-chorales-7": (
        "6b3fd56c8a8dd93951f44800bb14d2087084b8cc1e80cf0c8c9020c6c2fdba64",
        "a2f0dde7a8a4005571326e78f0e1fa10b418477e0d7f765e68048901202d1994",
    ),
    "wir-bach-chorales-8": (
        "6f049790441f8f301ba83653bda79d0b13d2d6e18de1d1416758ada692d40758",
        "89b527da3439fcfaf49e22ebba367bdcedbd1c624bf49759f2b30f7db789be4c",
    ),
    "wir-bach-chorales-9": (
        "3af267a7b70108604e1f4f50f5dc8343c492f59bb5bd81a32d5a03dbc3cd0688",
        "03f27251df1e731d9f0ba2ce61c5768dccda2894517e6a9b658b1fbea2f004af",
    ),
    "wir-bach-chorales-10": (
        "e948916392de72b3edb8c68acfbeb4584784a46feff738613ba5f843615f14ad",
        "3d7f458d1f7588de2c664a9aaefe287937be807355eeb708db38caab98d3bef7",
    ),
    "wir-bach-chorales-12": (
        "8d7abed480ec86dab6d6319adcd84cad95648a8b99b159a0415f2ac98fc74ac4",
        "b3c3257ceec1d28f6d7408dc34f5ffc8876fa985aa864f7e7af1287aba626925",
    ),
    "wir-bach-chorales-13": (
        "0006958014fce3bdc0941df7e8ca84090247e774916fef80bf77729de98de655",
        "b1a1a662561edcdd36ab6da4be1512878f06b5bd1173e9d6c6c8df549b418a89",
    ),
    "wir-bach-chorales-14": (
        "946d12117ef07dcae2fe9f081375a6fe75234517d804f16063c5a52e534a69e5",
        "73cba71862be12e5c432052da978a47ef2d3d7c24de2c1860a5400b573c33008",
    ),
    "wir-bach-chorales-16": (
        "c8669efd7e6a3f6803b422855562d7ce215187d06161e631f75c866b687ad531",
        "c59e795c3a5ad1a8adde9e6a096029bcd9b39dffb2497c3fa64d62746244e8af",
    ),
    "wir-bach-chorales-17": (
        "b00169557f728629aff44630c92b614873838d2af1018e5c5899b0b4ac5952b6",
        "67ad121175d7c1784fe5ce42ef4bc150b122f24781c5562ba30ddac7444b6d49",
    ),
    "wir-bach-chorales-18": (
        "0a0f8d895d5f32301bf901b1baf42d7057401cc821444bbd4d6efeeec4915499",
        "e2d2baa4f9215f6db06eee3e589d1fba68bc98536e55a82fb287752d64f436e2",
    ),
    "wir-bach-chorales-19": (
        "91e00c1cf1aaf5528887a1192784530ab6305cb25c4ffc0e4a8629feb137bc27",
        "94c548efe4ae90dbbf557b1ead77f0a99f9474be2869c93ccfb007b097503a4f",
    ),
    "wir-bach-chorales-20": (
        "8231549e33b86c3a1ec87792aae5044ef778b36a6a53494135410abf84e3ac63",
        "0b16559b20595697aa796aed77f71c7291e008f30a82ebe228a5b1b7c0d9ea4b",
    ),
    "wir-monteverdi-madrigals-book-5-8": (
        "76c8083d5bd1ae974f3eb0aaf9fcd6156024e6dcbce41b4c2e163b4ef9178598",
        "7a88a005cd06a981127fe6ea033eca62fa8a21924273dc9c96c3fd237580303f",
    ),
    "wir-monteverdi-madrigals-book-5-7": (
        "a6fd38ef16217e2829f2570188528858ed457b2cd1fc75d4cef4ddc2269f8e0f",
        "9eca939b49836c3354a3366a1596e9243cc2d0e61ed1d78ab6b22b3c38a94a1f",
    ),
    "wir-monteverdi-madrigals-book-5-5": (
        "c3045d2c0f8e2bf30357428f08ae15d004e48b7d8cb6913a1f997409724b2fae",
        "f31452dfa4c3e2e21e88f37838f35291ba15f7087088322fc9c5e1e8518427de",
    ),
    "wir-monteverdi-madrigals-book-5-4": (
        "62a22ab7a191ab87fa167cb5d2537be18511d9a93038b0267311470189b03491",
        "ac05c17311a4a3f9093e3d6573e530412bc7ededc7fe726ff7d42b40a2b79ff9",
    ),
    "wir-monteverdi-madrigals-book-4-11": (
        "4a8d58bc568fc8eb83f38107de8d40ff2b576be4552235a7dd74e5682ff07a64",
        "bfde30deab672367a7a07c4f3930861aa4ad7d76167814415e795ab8c519d156",
    ),
    "wir-monteverdi-madrigals-book-4-19": (
        "6f30ac26cd686a54a958b01439320e6e935926717a5b04739adb70d77cb9cf5a",
        "7d93782f4218edd8cea2e359fceab04e9b805070171a1d0cd3ac5405768dfcf1",
    ),
    "wir-monteverdi-madrigals-book-4-10": (
        "da61b8104fad791b814b52a63ca4a0caaa03e4391cbff9e90958bffa7979d025",
        "a64635737d720639076c1b28b6cd7b5ff8388aefe0b78ebe57411f22a2b3da9d",
    ),
    "wir-monteverdi-madrigals-book-4-12": (
        "0860884bc72f5e5203bf1becde0ab864cd5adb127ea20b3b65c1a1e74e8b329f",
        "82fa6170c9a0df44ceb1ffb01494cd3cd1f3d31fb73f7b5d460e8795c6db3b80",
    ),
    "wir-monteverdi-madrigals-book-4-13": (
        "9de539af3b2c16f921a9fd9e092b2fc2330e5a56d7d8355a1603fd4eeb12a6a4",
        "e08d7d8fbf0508197602fdcd27499596c7ba139ac7686932de9bb1e7ea262d8a",
    ),
    "wir-monteverdi-madrigals-book-3-15": (
        "b715473bdcbfc2fd08b4312b4148174defac6fbe626c1e8df53d7d118a863ac6",
        "146fc249de867a0c1ba96c862b64ecf900338a02818ae88daabbf34b55c9dc32",
    ),
    "wir-monteverdi-madrigals-book-3-8": (
        "c189f7a795ec1dd9aa14d82802b89834cabacddd1a5c5827faee49c8ec15f96c",
        "c96e59539d15d9dd670dde47ef9180e187130546f2c64895813659252fa52ec2",
    ),
    "wir-monteverdi-madrigals-book-3-3": (
        "4bdf10fab45e985e5f3bee5791682c7ee003ee8a9b98ba635c407a70f9e82245",
        "061574e53aecf40a58990479f6c7286ddc87c1eedf7cbe12ab1af24b0144f75f",
    ),
    "wir-monteverdi-madrigals-book-3-11": (
        "551cb2ef8ab97b76403506f2eac3bf77674d9fd65fa4702d369c54f1decf8eda",
        "2334eb8c96b44d6c1dcecc3dae45388e07ec18946af18685023f8cc04d906256",
    ),
    "wir-monteverdi-madrigals-book-3-19": (
        "cf2ce56441550ca4037df2f09e5841796aa74ffdee9c93e9fc5a010701ea1dfa",
        "ae39f9451b2c36d64c240cc12001b35038d65289c9f624b698cc564a9ace6959",
    ),
    "wir-monteverdi-madrigals-book-3-9": (
        "23b79c003c5c76621aa3ec2be0f5e104ab63cdf99f3872b41e86bfcb5fb744d3",
        "a7fccbb7331874d2c98674b32121e99862725bb454f7d60da8737b241ab86a37",
    ),
    "wir-monteverdi-madrigals-book-3-1": (
        "767e0531d31825d89fa91487ba1f3c629a6726c070bbdeceea48b5454fcfb8bd",
        "d4f7bb23242f3a0992d56ab56c4baf803cbd431cadc6af40ef04ace2337af94a",
    ),
    "wir-monteverdi-madrigals-book-3-6": (
        "ee8fe2032f57c974580b9a35b437fc44c6c02a522ba6def8813d6483870ccb2d",
        "3c4f27731d5ef8dd7b9a4351fd1dbf157382983e1ef7e953487303e1471c3019",
    ),
    "wir-monteverdi-madrigals-book-3-10": (
        "a9d884caafff74583526f6db538a547237d6a79654676b157ac15facc82bb84c",
        "6c2467f4e1dfca9e8d493018bfa206fba02133037eda214ce63185b39e67a0fa",
    ),
    "wir-monteverdi-madrigals-book-3-14": (
        "a8d8bd6c564b3fe317e61332e17c5afa2b9bb12fb8900f1cfaf486792e5fad93",
        "46175523f5f5b9a0656b5a038be62bda7b517dc9d084517eab711f099cef4d7a",
    ),
    "wir-monteverdi-madrigals-book-3-13": (
        "c1731fd3d9ae75885c1dfb0f92a72273bd46f420ebda3ec73a187d01b428a2ef",
        "daac039b636a60e41905d0947c642aad49996c4e1cb9a5a08703841b63f6f608",
    ),
    "wir-variations-and-grounds-bach-b-minor-mass-bwv232-crucifixus": (
        "ae7135de01dd3abc949e631ae8629c6c856855d2449880ba62f982d3e84082be",
        "3b3171c86e95c5382f59b3468e57faaf5cb55245f1fc0884fe34f07381052fe9",
    ),
    "tavern-beethoven-op34-a": (
        "83be3d2d6fd1151f033f862d5138e8626a88b07fed8e1c982c656bef22803bae",
        "5861d5ab00e2e780b1ad7683d06d9224895bdc47b7115634d7ea504b3ca1837e",
    ),
    "tavern-beethoven-op34-b": (
        "01ca40551717c82172f65f2b208bdd4966a2a0f761b12025887243f2b5a39c0d",
        "5861d5ab00e2e780b1ad7683d06d9224895bdc47b7115634d7ea504b3ca1837e",
    ),
    "tavern-beethoven-op76-a": (
        "0cca62603731f0a93d02a0bac690d2037e3d7b017c50d790766c0fa4ec2b31a6",
        "e4c409445cb1202b4a1ef003d1a5338e68f673460a7ee24bde5768f96d0ff439",
    ),
    "tavern-beethoven-op76-b": (
        "bc004e0ea7c9041b9e6f7cc35b28cf960b56cd1de41c59d07a6e22c1ae5ca5f8",
        "e4c409445cb1202b4a1ef003d1a5338e68f673460a7ee24bde5768f96d0ff439",
    ),
    "tavern-beethoven-woo-63-a": (
        "45307dd39336e6d32c7d99211553518d4503f82a75c6581f79b21ea06cb873c9",
        "33e1be3acc7428480fd744a9800b7228af06e88db40c062f6673411f53115492",
    ),
    "tavern-beethoven-woo-63-b": (
        "7f469fb57039e1ae07620a338ccdb899806a0688d5da5469f39eb59722d62b03",
        "33e1be3acc7428480fd744a9800b7228af06e88db40c062f6673411f53115492",
    ),
    "tavern-beethoven-woo-64-a": (
        "680405a0e8f5cadeefe09872f3898bed2cf02353614610e04806124e3492f287",
        "af5599e6fc866ee03d009604f9b2215e30918d8132910b85d87b03875dabd108",
    ),
    "tavern-beethoven-woo-64-b": (
        "ee344dc6552195a1e509d398b08ef8590fdac3adf1af090b36dbfdbed1a278bb",
        "af5599e6fc866ee03d009604f9b2215e30918d8132910b85d87b03875dabd108",
    ),
    "tavern-beethoven-woo-65-a": (
        "d313909df98e9064579663bee5f45410b3e0291c149db53ee132606892926463",
        "93a26e84787710f2796f259afe6e7419ae71f278da1776134ac34f16b528b6b0",
    ),
    "tavern-beethoven-woo-65-b": (
        "d9f1624906d6460acf3df5c392fbe77a70c7dec5dfae8a2b3b578e7fe8f9da11",
        "93a26e84787710f2796f259afe6e7419ae71f278da1776134ac34f16b528b6b0",
    ),
    "tavern-beethoven-woo-66-a": (
        "700a48228bd9103d326da773f34804c90b94aa373b830cae08042c1d9d1239ec",
        "5131be2044d990e8700e2e841596148f7315ffb588ef5150eb3132d44edfede6",
    ),
    "tavern-beethoven-woo-66-b": (
        "4f79ab228a3340180c32dd385980ea40e0c97cd879a5582bd4a082fd6f4d7ac8",
        "5131be2044d990e8700e2e841596148f7315ffb588ef5150eb3132d44edfede6",
    ),
    "tavern-beethoven-woo-68-a": (
        "53d980c2923c31b8859682a2a5f9b2b8bd2cb6be128cdd3192c541f33d844082",
        "23232501106d3dbdf443f35859ae3c4f876c30712eab68f0c3a730d3e4e893f1",
    ),
    "tavern-beethoven-woo-68-b": (
        "6ed66d44b38eeb1c00abc963d537a045e90e0dfa70cde24b7891fd29d00c8eff",
        "23232501106d3dbdf443f35859ae3c4f876c30712eab68f0c3a730d3e4e893f1",
    ),
    "tavern-beethoven-woo-69-a": (
        "d194fe71228a0de08cea04c1061a6dd08e2577e6f2e20d641d40a89586a23877",
        "98122e35995cd879279d2cbf72ff2f396538a47b01c220d539ead79f6bd3e0ab",
    ),
    "tavern-beethoven-woo-69-b": (
        "1507f6b34f88d39e91cb56ca83236e02e23eb1f4fcd8f66f6a78d9f943779962",
        "98122e35995cd879279d2cbf72ff2f396538a47b01c220d539ead79f6bd3e0ab",
    ),
    "tavern-beethoven-woo-70-a": (
        "645bd6068c6f54f79facfdd8713fed25dc8e1dcfd1e1305b970396785179f4d0",
        "e79485e8ab80189c526e814fc962f0d151770ec526cb73a24e67b772494624a1",
    ),
    "tavern-beethoven-woo-70-b": (
        "ef7222c7a11472087031699fec035adceba89745d4100cfb23d1346d4388b1b6",
        "e79485e8ab80189c526e814fc962f0d151770ec526cb73a24e67b772494624a1",
    ),
    "tavern-beethoven-woo-71-a": (
        "500af6258f12ed776ba6d23d3a0de75b140012988bf06768cd908589abb2c7ea",
        "b9df14cf78d1c7768dee1a61a6d98f782b682d112198d6bae6d4a3e2165c097f",
    ),
    "tavern-beethoven-woo-71-b": (
        "8a99335021be48bb28e4067e2e0207edfe1847f79a3c048828c98b8cb3bb87f2",
        "b9df14cf78d1c7768dee1a61a6d98f782b682d112198d6bae6d4a3e2165c097f",
    ),
    "tavern-beethoven-woo-72-a": (
        "d9accfef333dacbe9a1642120cbf579430c7ced4603e79c88aee4eb319eb99f0",
        "6d4fdccf73c71bd4643d734d325e4c305c318005cad8f447f118ef329e8f1c4f",
    ),
    "tavern-beethoven-woo-72-b": (
        "55517da561063f340b167229354b83e3d6f6057491ffdd1c0c559c5a17e36ad2",
        "6d4fdccf73c71bd4643d734d325e4c305c318005cad8f447f118ef329e8f1c4f",
    ),
    "tavern-beethoven-woo-73-a": (
        "9eef326b406b4489b2e7771312497ccf8008d039101b837aa6789c834c79955a",
        "bb347a050c5eed17af524c5a423ca0afadc6a540335fbb5b4c9cec62466499b7",
    ),
    "tavern-beethoven-woo-73-b": (
        "19a378472c96dcfdf1ef2ce29dae3dd9a29236884d044ead2843e1cf1bbf6198",
        "bb347a050c5eed17af524c5a423ca0afadc6a540335fbb5b4c9cec62466499b7",
    ),
    "tavern-beethoven-woo-75-a": (
        "f05ec6696d58cc5c5a9a1d05760fd4ed7677920580e0dc1647445bb41047a85d",
        "ac1378b7fcfb5f7d26ba9d691a17ba9d81919d303591b01495d8c52f25d523c1",
    ),
    "tavern-beethoven-woo-75-b": (
        "32a2e4ef0ea4bb03b2b88e88d1e449ff43e9ee6cd8fe9ce441cff49b27114678",
        "ac1378b7fcfb5f7d26ba9d691a17ba9d81919d303591b01495d8c52f25d523c1",
    ),
    "tavern-beethoven-woo-76-a": (
        "00c0aee8a5478c7964b573f61bc42f199b82fe9e2d3d2cdd4815b2acf754a4fe",
        "39085eb6b13b1db359f1ff21adb7011d088c9538cda3c02e27cd0093f2f377ca",
    ),
    "tavern-beethoven-woo-76-b": (
        "2d57df24850b0c593ff731a37c507ebbb9f6b199e6a8b9f8d7a628dbb31dab3d",
        "39085eb6b13b1db359f1ff21adb7011d088c9538cda3c02e27cd0093f2f377ca",
    ),
    "tavern-beethoven-woo-77-a": (
        "973d1d8e72175e71bf23ad3a352b5f8136d829a3171324eac34ad77e15f02b09",
        "7369bda4c83d5300b71f9fab053f70063ea935041530bd6a31b75a4b194fe200",
    ),
    "tavern-beethoven-woo-77-b": (
        "4c84ed74ee4ca912ef7e7f4a1d9e2639202f4a38f75963c48b152e790a2384c9",
        "7369bda4c83d5300b71f9fab053f70063ea935041530bd6a31b75a4b194fe200",
    ),
    "tavern-beethoven-woo-78-a": (
        "5c992cc77ba94594d395b4ffc55acbce2dc277b8fbfc41686f88f78ddf3dcb88",
        "28827978fca3c932d022bdb8c7b4af01a2284b355a7986b17694f1b33e8392f4",
    ),
    "tavern-beethoven-woo-78-b": (
        "39487d3c2047a2d052d84454c73639cde7b6372ce61a3b6768d6559b244de84c",
        "28827978fca3c932d022bdb8c7b4af01a2284b355a7986b17694f1b33e8392f4",
    ),
    "tavern-beethoven-woo-80-a": (
        "e047e313589220e0eb1c3617f0bf1df56d758bde33872df1897910095b6b74f5",
        "9b4721348e35cfa13a56492acaaced50f7c54adb6eb9e3ede5633a1948fa9a94",
    ),
    "tavern-beethoven-woo-80-b": (
        "eab18b188d19b62206a91d591e705fef3b6a43dc8ce49f48a8a19cd799155541",
        "9b4721348e35cfa13a56492acaaced50f7c54adb6eb9e3ede5633a1948fa9a94",
    ),
    "tavern-mozart-k025-a": (
        "e2baf195ace6666d0edd0a860b8873b767d9af48496d0b1587f9fef7d8ed1dfd",
        "61c8d784a4e495b8cff62a5d23e7b814014ca23b034eeb662eeea8c35f3a4d4b",
    ),
    "tavern-mozart-k025-b": (
        "62c014b80c27e194af51cc7e1ec049f9a1459e7e5f3194516366401fca07bb30",
        "61c8d784a4e495b8cff62a5d23e7b814014ca23b034eeb662eeea8c35f3a4d4b",
    ),
    "tavern-mozart-k179-a": (
        "fab75e9cd0740f8255b4d29161ff6c7d0ef223cb67c63d10afda96dac2cb92ba",
        "3ea9b1aa70d3929f468606712c9c49603795dea551744515309b45be25fa5ba4",
    ),
    "tavern-mozart-k179-b": (
        "4897f2cc180a2260b86012c443a51266a3e1815d64a6e5679d830b15bd8ed2d8",
        "3ea9b1aa70d3929f468606712c9c49603795dea551744515309b45be25fa5ba4",
    ),
    "tavern-mozart-k265-a": (
        "ed544effc9d6dc74123380be776586139143150df61381aef5bdcad3ccc17430",
        "baa693517709b8fdeac51c0538bf7b67b78f9f3866827d8eed7a2a38a1bb0268",
    ),
    "tavern-mozart-k265-b": (
        "a510269d11207126617643fc4ef46d7e56710cf0154e9ccc61a3802c908a5139",
        "baa693517709b8fdeac51c0538bf7b67b78f9f3866827d8eed7a2a38a1bb0268",
    ),
    "tavern-mozart-k353-a": (
        "c896ca3d88fd0eaf7c96fb945018dde7d168d0595cd8ed59b3a6e73f93dc671c",
        "fe11a55c25879f5a48e08c30fda79e1225cc8fec8e8eb837d853bf0328d7d7d0",
    ),
    "tavern-mozart-k353-b": (
        "6a521d7a1ad97ada9d12132870182504ddcd90ccdf8360efae95a9a66280e13a",
        "fe11a55c25879f5a48e08c30fda79e1225cc8fec8e8eb837d853bf0328d7d7d0",
    ),
    "tavern-mozart-k354-a": (
        "513670cae9a9ddef12228b101cb3e173f3e5be41f182d8a6c9ed7845b479b572",
        "5bf9e7d398d2b8356efba6c3889b941908b87471d03a92ddb2a92b7f09fb4f8f",
    ),
    "tavern-mozart-k354-b": (
        "b959c24ab8f587477a56d7ef6a62dba4533250e8ea158c8616f99ecbf07a7ce6",
        "5bf9e7d398d2b8356efba6c3889b941908b87471d03a92ddb2a92b7f09fb4f8f",
    ),
    "tavern-mozart-k398-a": (
        "96de8afd21b52b8100574b05e6214aa7ebc07f00dc487d903a488131ef11f667",
        "033d597089eb78f2e9f626f3a663291f6a59ccb9c662b6d0fc1e3fece122aec2",
    ),
    "tavern-mozart-k398-b": (
        "7fd10b60cdeb5d6e3ca74ad0dbe0ac160c59cba5633f54e4f4e4731a3dc143db",
        "033d597089eb78f2e9f626f3a663291f6a59ccb9c662b6d0fc1e3fece122aec2",
    ),
    "tavern-mozart-k455-a": (
        "c85d445bcacfe62ec5ec91d1d18ded89bdc540f9cbf2787c30bd1208eff9fe80",
        "c386b61c085700d10a784083b5a5ccd9690b76d0b3098655c17e104035143265",
    ),
    "tavern-mozart-k455-b": (
        "b0bc93c8471d31bcf7d5fd5939065b2a7b2545191c04dcc3268abc1ac09e4230",
        "c386b61c085700d10a784083b5a5ccd9690b76d0b3098655c17e104035143265",
    ),
    "tavern-mozart-k501-a": (
        "0ab5f7fec1719907c084035aaee1785231e86159cde3a6414bc7d2655e0df50d",
        "578ea6a542e61617184a3961175b48f4943e29770453524ed77eb3026fa18f79",
    ),
    "tavern-mozart-k501-b": (
        "00c6691778c20c994234b82de3fcaeea31ca95e46224aad697dd20b7b88ad204",
        "578ea6a542e61617184a3961175b48f4943e29770453524ed77eb3026fa18f79",
    ),
    "tavern-mozart-k573-a": (
        "a2862e1d8eb20f39185d74dff9c88992ab2a19038069bbd9e80726609a5da50b",
        "19510fcac10413295bf4dbc0c845b75c544c6e56428fcb3060e030153a44ae77",
    ),
    "tavern-mozart-k573-b": (
        "b3c4a27e8ba78b15fc6ef2441fe2c846ef41010537a34e9c3623178b73eeb5f1",
        "19510fcac10413295bf4dbc0c845b75c544c6e56428fcb3060e030153a44ae77",
    ),
    "tavern-mozart-k613-a": (
        "fcb4c8455c1b2596543270e37ddae647fceba651d259d578b771035dfb0dc872",
        "1c423cb470a351e5515f54430a7e18db6f1d0b74ce922a56f3ff39838a5cfef6",
    ),
    "tavern-mozart-k613-b": (
        "436bbee85c8f62daffd572a54193b21759d5591177717f1d5bc860b9b255ce09",
        "1c423cb470a351e5515f54430a7e18db6f1d0b74ce922a56f3ff39838a5cfef6",
    ),
    "wir-variations-and-grounds-purcell-sonata-z807": (
        "7038285b6d0a15ccae85d505953cfa3ce4fd227615ea62d033574be89b0198fe",
        "793148b71ded02995e277cc0442be7fbc836b07142450f323294bc2dd7073f46",
    ),
    "wir-variations-and-grounds-purcell-chacony-z730": (
        "6695a88b4e668ffb013ef421237bd4dde74fdeee05064d030786f5da278faf12",
        "c6b27133de0ddebcac0827fda1bf0dde76ecdfaadda3edad200857eb58fbc7f1",
    ),
    "abc-op18-no1-1": (
        "39361e76e97d7e2018666b625973239262987c01d9f1cc8bbe8319602ee61848",
        "2d7c8026b5ab651dcce96ac368a8e92bea5674f74aef3e163511dcdf8a311a43",
    ),
    "abc-op18-no1-2": (
        "d61ce5bbdbd807d5dfb6877b10be9089c48b7b8fe8644c06ceea289b41b92b91",
        "36870c0293d95045a1df62aa95bfee0dce6698441453e4d418429f0f92006868",
    ),
    "abc-op18-no1-3": (
        "d25359448d71169d34577e6ec30a1df7d4bd1c8c7decdb99847227323c553055",
        "9620715250932675f6e91fced27c06701b17a58cbbc1fb1a4083843212c45d49",
    ),
    "abc-op18-no1-4": (
        "f805200d9e23df0985098ae5c2b83794b08d31a2e234c9be553e1d0bc6d33007",
        "b095353961c03b9b47df7e1a894f4bc73928a7fc8bd6713baf1e8bf0d15f6f22",
    ),
    "abc-op18-no2-1": (
        "ee9bdc9b2d150372671f8c2e1e6ac39e982c1359edcae2eb2a9744b845d79a71",
        "594fc8d098779e4b545b2e4d8852cb468ceba480388c891cfd7f8a1edadbb4eb",
    ),
    "abc-op18-no2-2": (
        "96649a11bb4bc9daac160cd331e776d5f826fa3be4b49c527fcfae164c7d915a",
        "7eb64cbeaa06a88c98c53dae0eaef39f12e9e47d08d63f98ec58f6744970ced2",
    ),
    "abc-op18-no2-3": (
        "a748734a2afe87b67a1cc045f846ed661ceb85fc47a4ff2f235ebff5230b4dab",
        "9b22cd62745e3f3bf39a9a11f3dc128146f5d260c4fcb579accb9e6e57825c18",
    ),
    "abc-op18-no2-4": (
        "32bb960f59d826be5e81795e49f360592697a6b18dd679d0dabedba2b713211d",
        "e40fc2e94e36cbf2758e6f634772223ba960b06d9edccc9678e52a768dffd9bb",
    ),
    "abc-op18-no3-1": (
        "ecfe4abe45199d0aeac64116bf7f99bc847bc6a8d2eb9998a821d15057c223ff",
        "d690d70769a633b8d231f634adcad44294196a7f3556e86a120af1bb071759ac",
    ),
    "abc-op18-no3-2": (
        "fb6ef22a9ee6761e6defbde4bc5f3a45d95a1c684392a37ff73c417a04df0cc4",
        "f8e10502019d8658ec780a035175c88998f23578a69450c02994e9ffc5a6a260",
    ),
    "abc-op18-no3-3": (
        "d373b1f1655910700809a5aac1a81dca1eb24f14623947cf5be561508e61f117",
        "4326618af4bdddaa5e00d8c19760e40fac44cb29d30d77c2ff7fe0d3e63d5ae5",
    ),
    "abc-op18-no3-4": (
        "e4d09a1702560064a28e4c29500156a90f4ec48e4a88871c5bb79b21a13ed5f2",
        "d68070f9ed18d78cdbbbb3dfb04357d8bcb909c36f36551f8720ca1f382d22bc",
    ),
    "abc-op18-no4-1": (
        "326bf93c182017f1975e57a39aa9f09adf41381fb688dee8abe1c30e2ae74c97",
        "567f27203b2c9c2fad8f6d33d64ea97b2aec26eec74b26b2474a3d66b70c1b13",
    ),
    "abc-op18-no4-2": (
        "e1df5c82fc99ea1af5ece33795b2341c6f9e4bc9a9780bdc275a5c5d9a1a7637",
        "dbf8a9e5cd157dd0a19aac01b2b194d6b934f5203d55ef4eb03448965ea24256",
    ),
    "abc-op18-no4-3": (
        "1d296d628c319526aae4e919878ae7d100dfd30cf55ee6562171a4855c55dbe5",
        "074d49f50ae13659cfed366192c2d449e877e148dbfa7a4c0a4b688eaac56b04",
    ),
    "abc-op18-no4-4": (
        "7de076f627bab1b850712318292a71ed1354eab65a6f07d628bc9bc161c19d9d",
        "189df8b618ff1b4a66800883c3db169288b4b2a66f0f56cf76956f3f918d6467",
    ),
    "abc-op18-no5-1": (
        "5d0f0c46aef25b96b9f2a3ef915eab216daa5798ebe07367140ac6d8ef4fa86f",
        "075c19977b2cb73e8c39850a62f0e44a6599f8a5511044c1cc9fe0508fe46d9d",
    ),
    "abc-op18-no5-2": (
        "dfc32654331427fec14eda22c3095f929e77ba4a2ae97bda873434a7bf8f5ffa",
        "8f05001e46513f02d240b77798c2973e35a9ac9b4b0fad57e41d20445f578e4f",
    ),
    "abc-op18-no5-3": (
        "5979e48018f6703ee3824cdeb6d6d01ed7d843b28deb302c48febb78f50a4d6d",
        "65f6c224871d8a1e7bec5d63ca5334b70b4afc8a961fce28f8d0ece66fcca20a",
    ),
    "abc-op18-no5-4": (
        "6c7e3eebbad6ff860add1f9323f04a7e2f7e938f034d6da7d35111c9a24c5b62",
        "f88e99ba0568f3a689e3ec45a4c437bf8099ac3fbb3247a353c5937884b373ec",
    ),
    "abc-op18-no6-1": (
        "b9cb515dc570ec6b220520de6492791ce59ce5fdbeb44a50657d32689a3acc3d",
        "57e81ca6a54fd6245563a2e2683c274426057ac7a8c132ae7ea57836696b382f",
    ),
    "abc-op18-no6-2": (
        "dc25a5d7fb8a5003cb8cf458a973950316913d730e7c61d68be00ec17239bea2",
        "c3af32b87fb5eaba5ba69031b417d7d3b46b7bdec477c3cf0088728955026030",
    ),
    "abc-op18-no6-3": (
        "eefc7a15762c24dd4aa827b83681f0cd41682d5909b7114de401700f914c1aa8",
        "3e386842e1a45cf607a506bf8784b72e2b69bc388b6640c753b28ca487b3db07",
    ),
    "abc-op18-no6-4": (
        "68df29bb08c5f4552a4a5da10a8e8279cd194699b8c716312038589ffd36765f",
        "979774c0513f10f3f98e14e338e64bc2064c77f6c3b1fe9c4e872eecb31bfb54",
    ),
    "abc-op59-no1-1": (
        "c4f49ebf6fad8be40f9b27460eb6b35172035cd88ac97c35d3753271522d04b1",
        "77a61f48d302374f51b0cf6bb90a5dd91a77f775e1b193753da12b05f1e1e285",
    ),
    "abc-op59-no1-2": (
        "f31f8b6e5d2a2f5da9ce29e67778bf720f7fef9d83fdf2a5962f11b7dfd22751",
        "57b5d7c033f5a24ee6e45bb02ef98db3662f11855d0ab3f901a568bc06389c08",
    ),
    "abc-op59-no1-3": (
        "1209af9fd4496e36fd7a7964150d3edbe87208ec1ef87c2eeea14c167fc96b21",
        "49aef85ac2ab7ca0b27589e7923a95c846e53d2f79c498330bd3d9dfb386ea36",
    ),
    "abc-op59-no1-4": (
        "e76616f8c692223fbf100f7de72a6898776b1730be1da9a8059f1a51dbf1344c",
        "3c2e2eb10772b218445bf3526fa547a3573fe29b4621966f56dd4cf3c22f3f63",
    ),
    "abc-op59-no2-1": (
        "db52cd38fed05c1d659453ecbe5822ae9bdb02309c04c2fcff088f43dbdb8f02",
        "62f875c1e766ef3a9d89b2507330d8920193df5999f7ad202758414600b586a4",
    ),
    "abc-op59-no2-2": (
        "a7c1c96583855cdcdd9cf7863652355a5424d13f83ffcaf84ba409beac77675e",
        "8e7b0033d7a1de195e16cb3684851f83227fc5317e1de7d3092669a929475df9",
    ),
    "abc-op59-no2-3": (
        "da51ab840bcacd250296e268c7ed0bca84531208293aedcf62f0f17363bb0c9b",
        "744148fbdb8a24119dab6db57917676684da2298286a11e29d14ff0cc18311bd",
    ),
    "abc-op59-no2-4": (
        "89ebfa7d3b837974719add21f090a364aaf6c235178866f0ee78f8178d5c7016",
        "76d74f876c7e20263ce3635efc623c94ac95093ddcea7df9dcd769ead8767346",
    ),
    "abc-op59-no3-1": (
        "6c7ea1553a4252580ccafcdfdb7f31d449d430c101275e49a424eda3d310a82a",
        "e805aae597de1a0f02026771eaf8c9235db6b47f1e755c68253d459fad43dec6",
    ),
    "abc-op59-no3-2": (
        "f61424b6feb6595f10390be1d424c92903cef149a75e5375b36f06d3325dc5ad",
        "0d52886089e404836bd6e64d65def0c6eb2607effd7d74ae4a7783a6041d068c",
    ),
    "abc-op59-no3-3": (
        "246c1b896374c3d65925f9e873e9bd29819d4f58d545abb669f6144e28c7a4e7",
        "e3f502bf6f833a2f118196f53d3d55270020da23ccc778197ef2190bb781e5fd",
    ),
    "abc-op59-no3-4": (
        "f09d6c852d3fb3b524f909c67162db3441ff7112094d0451fddcca59db412275",
        "e2c7181fe9ddbe59980d031055a07a0300d30d6a8594973762ae32b12ae37868",
    ),
    "abc-op74-1": (
        "0d1e818766003453a760270f553103bd2ab8bccf557b9b0b5e0a03699d8339ea",
        "34d23412f88782ea82472a85cfceea81f79b292a72c0de2925b46259e78a15f5",
    ),
    "abc-op74-2": (
        "ca3146b0d8ac20cb44c1e54c8ce765f4012714b97d06e820375cc6675586cd1a",
        "7bc4a1a306e55ac9d4e283b6d2ee74b6d423b4135eac9686b6e92cd47f5dbac4",
    ),
    "abc-op74-3": (
        "c183a9fbd2295f5b1e9f7e1d3286b5a2229dc04d905d92f9fe207eb4e8a3c994",
        "4e43b6201785c0af3867f7346b3c1e73002b6a16532f5baae95dfa0003232ab2",
    ),
    "abc-op74-4": (
        "65d83db4fa015ddc393ff414d568ddb12c10b2b5f55062789b64ae57ede585ad",
        "a30da8c452bab16869a3963d45d96d6ec9bb36b9105070dfdcde1817e399128e",
    ),
    "abc-op95-1": (
        "1f15de70417e4c7f56663006783eaac0015bda5a69bbf269f083e39b6630ee6d",
        "c302cec1b2839de8078d2e4c8745cb36ceddc272e51c143df47876dfec470edb",
    ),
    "abc-op95-2": (
        "f48133f272f15b42e672379b0ed82c46e5e1e32dbd4c068141ad3e2971d16383",
        "8d1d9c8a6b7b8bd300b09b251a5d14647de272163c79dbce6b02f4626db0d6d1",
    ),
    "abc-op95-3": (
        "7d8660885d28b58f490629b506df1edbf2cc4bf231fb261a0a849028e496630a",
        "91b1e71ea63c0226785e285909615b912602a4e8de0ff853b89e4f58be2c142b",
    ),
    "abc-op95-4": (
        "49ecd84d97a51cb9a6f0e253ea5aac52c42738c89db9f42c9247cbb8b53cd8d9",
        "37313c75590aedf11063ba5f6669ed7809446c307fd2b88e97ac467339184c7a",
    ),
    "abc-op127-1": (
        "11c0694d8488aeea2a9c880b3404e57833a4ea3bc43a0619831fd15aa189ce71",
        "8db198f6705681ef862629e3dace67ff3f2a35583c09c0057cd7e7fc95107200",
    ),
    "abc-op127-2": (
        "a990069e615e09cf36c10012a81d42833f5ab107dba85236254b789129a3af3d",
        "b520bd12c61d65b9a04c2f4e107f2cd7c091d0821d8dd3d13818bbfc7cc75118",
    ),
    "abc-op127-3": (
        "fc2fdc4c0252c20f17eb169a9c5b3667d39ff8eae66007be844e8fea2487c72a",
        "0717f211d13a7d267807115b045f3c741b39ac5c58d812e85dd4e5f1e0f603fb",
    ),
    "abc-op127-4": (
        "a013306853e3acaf380526e76f7931ac695a4466634b4ec4225eab3cdd05fe98",
        "ba6cf6c1712a321e0864aeefde116261b04b2430086c830cca7862df2a2e5699",
    ),
    "abc-op130-1": (
        "67a1b43255a2fb4093a7209205187a8e427b759ecbadc9187185dce9d8fe7261",
        "e8f352c8c8292eefe000c7034b437e90dab10c23276f85641216d437933022ba",
    ),
    "abc-op130-2": (
        "a37a02e18cef511c2c9c9df5ad669eedfa9163e5b6073022c25907544b73eefb",
        "be124ab13415a1f6d03f23d5d08daae28cad13714fa8b0b34efd743b8349b91c",
    ),
    "abc-op130-3": (
        "f817ee485f8a165f76d1eac549d9421410977671f08edf7a5c770c97afc47bd7",
        "2c922dea65bd3a9d6c9ed9db8f4cb07a04558a8dba28c6a43a534a153b934fdd",
    ),
    "abc-op130-4": (
        "37b8cae5e7e22b3f14d5820e98861572598e42f5f9d53adfe8f6d30ced7fea52",
        "d1cbfb7ff4f7f229debcdfeca6c8b1a359a5e087890cee79beb47db0c9a9fc59",
    ),
    "abc-op130-5": (
        "533d4be51c524426d37ea50414fe1f9923f2a98db9187dae7647a6c07fd5aeb5",
        "5a68d64e5b71551eb155e01578c6c8ccc9c9907f2a06f9ae643acc3f2aea24e0",
    ),
    "abc-op130-6": (
        "bbb9909727c4e4f217c62cd7e6ae655ce56554c67eedbdd1c7e7fbc30f583dda",
        "cd8c65e36493ca68b550698cb741ece0423b53286cdc94c36247aed57bbf91a0",
    ),
    "abc-op131-1": (
        "b1b9f78c63e5ab727c6199acda1984e85dbded7f1d41d654f325bc98df56c184",
        "7382374f8b749a49e04aca89bf14f2c521e9d2d365992e25908bf07cd7035098",
    ),
    "abc-op131-2": (
        "58fb1f4d30b2e1eda7f39e85ab549b194b5e6a8fc2259ebc3344d3265acf271b",
        "c9fce711026f906ab00eede550cbcd3f747fe5fcdc89f5aa8ad35abd3bde6270",
    ),
    "abc-op131-3": (
        "503a4fb782d18b74e32a95f0e0c870424d57ee88af160d8809856d350e0ce860",
        "46268bd270008b188bcb950258a11ba7c59fe7258739e6a5314f2fba7262405e",
    ),
    "abc-op131-4": (
        "a93f2865543f7702d59bd6713282b823499fbe0ba9505b8a3ac52948b2d2e42d",
        "4deaf334df73cee3a195fe423d64ded4654d6eba0b512ae829e03f744d718ff5",
    ),
    "abc-op131-5": (
        "f01ac5ccca7c477ac8ecfe3fda6e79aaebfd0b5c22ea891c974d5000a24f060d",
        "4a96321cf273c536aae4f7d83e853bd0e89ef21ed92d261e3855fa5a1bb27384",
    ),
    "abc-op131-6": (
        "d6a2f8f74fcba192fe69f62d12b04f700de52113419515c0aa02a1db151b723b",
        "3ccc823ea5380fffe118232163dcd44cd18658c2202901de92b8dc0d12937945",
    ),
    "abc-op131-7": (
        "fb78c2cd4cfd7da0f1ad491dd8b4c85e3cb7bb715dc217d2ed71d416a834f2fd",
        "8ca83d7c8482192b21654947384a2fbe1acbc4d5290501a4dced175394ed3606",
    ),
    "abc-op132-1": (
        "ff3241403834aed83da17be7615832bc95e0c7d4797b98f61ffd1355f1985271",
        "eb9e0d0d12d3d628df7964fc039d19cd143039b4f5039d6358122686150fdab1",
    ),
    "abc-op132-2": (
        "6d7bc38a745e1125e918c062fc6e3526e03c15a21ca6c50474409d93f3cc1731",
        "8d9077f0fcd07e83b594d6c36d8b96726256473f6993e4c0a3c3d9133a6e8c23",
    ),
    "abc-op132-3": (
        "c0cd1365e6379bf310a5b5855b527eed5f769c9e67c3559523f22b6449863580",
        "117d050891397dec4dc3a0456277e2a29f5ec97033e4343f388793b463ac4b24",
    ),
    "abc-op132-4": (
        "5dd45d2616df29d03e8c6cbcbbd991a25f2d8d0079d970581fe277f9e45d55d4",
        "700a2fe96ee9b1b9938f82ebd4a19f4ce901f9b7ee54a77daa6d91fbca3b83d1",
    ),
    "abc-op132-5": (
        "43d259fa18faea8ef580a3a72f2ba42d462fe3c08072eaa17f7af394f3bde9e4",
        "4d4052747526375d3efde2a4ec700fee0a7eb17b4ed0ea9a7fa2a3a04478eb23",
    ),
    "abc-op135-1": (
        "a63a4a62221fa40633567ed578862438e29a491c96960b6bbafa9218b6cdb052",
        "41259732ebaa8be9adcbbb37a5dcb735808a53e476d4e0f7c258bc5766efb95d",
    ),
    "abc-op135-2": (
        "0c255474379b39afce15c0dca4351f010bbf46174c7aae59a007026c30b42035",
        "564703d408870663a455d691ca4bf96e4de55b351f1c091a1e3ccd544e91a9b3",
    ),
    "abc-op135-3": (
        "9aa39b7ef5b28a065cb81baf6754d970fc79c7ea4829e51c411efc825189d440",
        "270a86071ce520e0896b0271c4df90af090d8e92f4b8bdbb1f2b5c44ef2a340b",
    ),
    "abc-op135-4": (
        "f5156b7221bfbcadf992d0c66d9524dace2b74e4d65c1af8cfbf6dea40b78531",
        "ddce344eee57b49593d38a96a099f1c8b8fec6b4e87e8982c3b51b522b4141b9",
    ),
    "haydnop20-no1-1": (
        "7aa1d448f9cbbecae0c93264de8372e50c6ca598d08a306fef97e496d62b7388",
        "93a60038d92b9b647af7301689726ed6d1178ba98471eb6a88f6c3a0ca674cff",
    ),
    "haydnop20-no1-2": (
        "b65e51cae1b3e7e121f32868fb015275fe67257d96586384e2dfa1e9f4c5ed31",
        "aa8c53110d6a4b9f875f0f436a0d8dc647805402645acfe181c2134cd201c834",
    ),
    "haydnop20-no1-3": (
        "feed6b60127773e0210c4737a86770a828ad072460ed27e16008bea8e10f6cc3",
        "5d6832019f68054eeff1025223ccb1a497cef4e18206fef4ad2c00459db0455a",
    ),
    "haydnop20-no1-4": (
        "99bd109f1d02177abfad93a205ebf8d8a4ce5fc6be4d5b6eb0e802c303b1d7c3",
        "ffd534d4747d77253b6940305d93950c57f72c4d955c890727b671e37097e4d6",
    ),
    "haydnop20-no2-1": (
        "a77788e6ef83bbd859c86451efb070d2fbd586f8aaed39379082b3adb119fc02",
        "11c7bc9e24724037ec7e26df686769804d463cb89814cc46e8d689d29482a0a3",
    ),
    "haydnop20-no2-2": (
        "fdbaae2d5b4b2d3931ccd3aff2cb886b65f66490babac84f7c2b4d2322f06900",
        "bc47bd17e1d785eeb53a5ee10d52b27628a6b5119f8595e3adc1aeed79aa5729",
    ),
    "haydnop20-no2-3": (
        "1994d04fe9b7a7d3237c51aef7d5ba3277273fde5b9b1e2dee553abeddb26ff3",
        "8150331e90c24a3f76380a1f0b0429b4b511b2c7544a79edd7db01c09f424399",
    ),
    "haydnop20-no2-4": (
        "b90d0634d89e47b04f3594d960044cfafb0aa8cdba8ab3963db3081aaace6d69",
        "f4de6257c5e7672f72e20fb9f1188f989f2e28164b4fa475b3eb6e01729dcabd",
    ),
    "haydnop20-no3-1": (
        "196540d24ac9cb092f80e642d9a6570bc1af5a79b36aa92607afd2b78f08fdbf",
        "47c16ba808b78330f96327ff4ea058c44011772e8608dfad240a40028cfa174b",
    ),
    "haydnop20-no3-2": (
        "c01c73d39728e9cc3872f71655f729ec613300f05d6dccd23ac937b33c1f5e2c",
        "2934d7cc93f658fdfd4d6770f6023e9ce46b84bd8f218afd6678c1406a0d3740",
    ),
    "haydnop20-no3-3": (
        "8345b0c954aa59c85e51b9d7fb31b9077de28f86d2a6b5de5617056bb3ee68bf",
        "41ea0248e5607377dde95b49c6fec550e3551c05908b7aec08964b0e34185e83",
    ),
    "haydnop20-no3-4": (
        "3e3926435d30b2c68e7a444a522a5b9f96065a6de5b57d80d10eb5305e5d29f8",
        "2006d6d15d6e3d210ee206b12f8204ae36dda7278123586583e6101150ec01c8",
    ),
    "haydnop20-no4-1": (
        "72e71752afc86ae270893832112773787de5350f30bffd8bb59d5ec36c7ee562",
        "86e48d7f08b5a65e25d7e4eb85a17d913159c0edcccf93e00608e72acf7b693e",
    ),
    "haydnop20-no4-2": (
        "1adad35d965aac5a0e080ea1429d0e3da7d5535e1941288bc7b948af28870986",
        "4b4ef74142001512035a44758d3ad36b9a54819890e0a10b447374f5141204aa",
    ),
    "haydnop20-no4-3": (
        "1101ea40af9129ec755a06b869820312891062cffa7de23cc5c930eb21f4d426",
        "36ca4b1e586b63134564327eaf4e4d48fd7cb336ddf2020717cbc8d6181cea51",
    ),
    "haydnop20-no4-4": (
        "068ee538fecdfe0bf3dd15cf3fcf109cd27b0121849bf2c6b4a052cd452a47b8",
        "e55aa47ff45aa5658d4d43e5eb2fe3b598ed880d55e72f62d27112032a3d4bc0",
    ),
    "haydnop20-no5-1": (
        "c27a030df59377542eb8b3759cd087f07bf1a344b78fdefb3f654c99da1270bd",
        "d8b3df87e2f8efac6ec6bad3b9a49f658f6ede16c38f4143d00ff999588e0237",
    ),
    "haydnop20-no5-2": (
        "cfb1737669f1243c68f24b59f8681ee86df33ca653851cc45825ae1b9ed99592",
        "aba428c570c7a0cc1eb16d90d93692d8bd925fff59a5062b8af3475f50fa2f11",
    ),
    "haydnop20-no5-3": (
        "44f9d1eb471b6e843519a8c5865a4898af8f9e43c578e7317eb8125dfc322126",
        "a2a95fd687a8475f033c93ac2f695d81c5e15bfeee20b8dbf23b44f0429784bc",
    ),
    "haydnop20-no5-4": (
        "b5e06c14de13751147f14565745d09e42bd28e87ab48d789d80498cbfdac19ea",
        "64fa12ed4abc9d9b9e2876c752182bc41d44ca239ea281b2a0719c6b70eb1793",
    ),
    "haydnop20-no6-1": (
        "90750027ed5297e4491e2ceeb705b085173ca6b7051acf0b253dee065807e5bf",
        "ee022bf3fa15d98e783d445d98a89964224be2d3be0e1e4b6adf9f64671930ce",
    ),
    "haydnop20-no6-2": (
        "0a07eed3a96e363ebf7c78f8d2cf55e62d56adf54cef8d65e1dd2a7b50eb3fe0",
        "03e9ac3d57e7afb17a656b8b232927a13747ffcdb4215f3dd1643b8ed776967c",
    ),
    "haydnop20-no6-3": (
        "69d9e51a69ff39af69561a4dd6e509107485de9bb44cdf6297d3153610fae4aa",
        "38ba283d5697062a0dead30ccb0b74e1d21c7ace5b901c2b2c4719ead2082d46",
    ),
    "haydnop20-no6-4": (
        "a06e13c1b6f738080c54d25b159a12528f726225be0ce69d2a034b80702ee547",
        "735842cb3da67892a9b03b86700c6f0e6dd376c2f95a75d4bc7fd4c2d98f4da6",
    ),
    "wir-orchestral-haydn-symphony-104-1": (
        "a062ec411150c608d9daf50130865dce70d3bead8bde7f08474037f5afd73c7e",
        "a9f82e3e7d25b03983142fd8b85447dee8190b3c9aa07245baf0f4da94eccb9e",
    ),
}

datasetTsvGT = """
	file	annotation	score	collection	split	misalignmentMean	qualityMean
0	bps-01-op002-no1-1	When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op002_No1/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_01_01.mxl	bps	test	0.0	0.11351395730706075
1	bps-14-op027-no2-moonlight-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op027_No2(Moonlight)/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_14_01.mxl	bps	test	0.0	0.03797101449275363
2	bps-23-op057-appassionata-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op057(Appassionata)/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_23_01.mxl	bps	test	0.0	0.06165236733396885
3	bps-15-op028-pastorale-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op028(Pastorale)/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_15_01.mxl	bps	test	0.0021691973969631237	0.10484454085321765
4	bps-10-op014-no2-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op014_No2/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_10_01.mxl	bps	test	0.0	0.10266832917705736
5	bps-25-op079-sonatina-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op079(Sonatina)/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_25_01.mxl	bps	test	0.0	0.09137645107794362
6	bps-07-op010-no3-1	When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op010_No3/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_07_01.mxl	bps	test	0.002904865649963689	0.180479302832244
7	abc-op74-3	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op74/3/analysis.txt	AlignedABC/op74_no10_mov3.mxl	abc	test	0.0	0.28371204001429084
8	abc-op127-2	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op127/2/analysis.txt	AlignedABC/op127_no12_mov2.mxl	abc	test	0.0	0.10595674486803519
9	abc-op95-3	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op95/3/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op95_no11_mov3.mxl	abc	test	0.0	0.13456521739130434
10	abc-op18-no6-3	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No6/3/analysis.txt	AlignedABC/op18_no6_mov3.mxl	abc	test	0.0	0.1189294403892944
11	abc-op59-no1-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No1/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no7_mov1.mxl	abc	test	0.0	0.09708125
12	abc-op18-no1-3	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No1/3/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no1_mov3.mxl	abc	test	0.006896551724137931	0.41931034482758617
13	abc-op135-2	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op135/2/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op135_no16_mov2.mxl	abc	test	0.0	0.2662029161603888
14	abc-op59-no2-3	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No2/3/analysis.txt	AlignedABC/op59_no8_mov3.mxl	abc	test	0.0	0.19146913580246913
15	abc-op18-no1-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No1/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no1_mov1.mxl	abc	test	0.044184189512909235	0.2307825392600479
16	abc-op74-4	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op74/4/analysis.txt	AlignedABC/op74_no10_mov4.mxl	abc	test	0.0	0.19668158567774938
17	tavern-beethoven-woo-77-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_77/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B077.mxl	tavern	test	0.0	0.15964912280701754
18	tavern-beethoven-woo-77-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_77/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B077.mxl	tavern	test	0.0	0.14278947368421052
19	tavern-beethoven-woo-75-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_75/analysis_A.txt	AlignedTavern/Beethoven/B075.mxl	tavern	test	0.0	0.17897058823529413
20	tavern-beethoven-woo-75-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_75/analysis_B.txt	AlignedTavern/Beethoven/B075.mxl	tavern	test	0.0	0.18115610859728506
21	tavern-beethoven-woo-78-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_78/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B078.mxl	tavern	test	0.0	0.15768737672583824
22	tavern-beethoven-woo-78-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_78/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B078.mxl	tavern	test	0.0	0.1648471400394477
23	tavern-beethoven-woo-70-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_70/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B070.mxl	tavern	test	0.0	0.10106679960119641
24	tavern-beethoven-woo-70-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_70/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B070.mxl	tavern	test	0.0	0.11136590229312066
25	haydnop20-no2-2	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No2/2/analysis.txt	haydn_op20_harm/op20/2/ii/op20n2-02.krn	haydnop20	test	0.0	0.1655753968253968
26	haydnop20-no3-4	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No3/4/analysis.txt	haydn_op20_harm/op20/3/iv/op20n3-04.krn	haydnop20	test	0.0	0.08282112845138057
27	haydnop20-no5-3	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No5/3/analysis.txt	haydn_op20_harm/op20/5/iii/op20n5-03.krn	haydnop20	test	0.0	0.050666666666666665
28	haydnop20-no6-4	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No6/4/analysis.txt	haydn_op20_harm/op20/6/iv/op20n6-04.krn	haydnop20	test	0.0	0.18105263157894735
29	wir-openscore-liedercorpus-schubert-die-schone-mullerin-d-795-12-pause	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Die_schöne_Müllerin,_D.795/12_Pause/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Die_schöne_Müllerin,_D.795/12_Pause/score.mxl	wir	test	0.0	0.021481481481481483
30	wir-openscore-liedercorpus-schubert-schwanengesang-d-957-08-der-atlas	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/08_Der_Atlas/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/08_Der_Atlas/score.mxl	wir	test	0.03571428571428571	0.05553571428571428
31	wir-openscore-liedercorpus-wolf-eichendorff-lieder-14-der-verzweifelte-liebhaber	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/14_Der_verzweifelte_Liebhaber/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/14_Der_verzweifelte_Liebhaber/score.mxl	wir	test	0.0	0.03258536585365854
32	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-16-die-alten-bosen-lieder	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/16_Die_alten,_bösen_Lieder/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/16_Die_alten,_bösen_Lieder/score.mxl	wir	test	0.020134228187919462	0.13159395973154364
33	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-10-hor-ich-das-liedchen-klingen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/10_Hör’_ich_das_Liedchen_klingen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/10_Hör’_ich_das_Liedchen_klingen/score.mxl	wir	test	0.9666666666666667	0.06670833333333333
34	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-04-wenn-ich-in-deine-augen-seh	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/04_Wenn_ich_in_deine_Augen_seh’/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/04_Wenn_ich_in_deine_Augen_seh’/score.mxl	wir	test	0.047619047619047616	0.0031746031746031746
35	wir-openscore-liedercorpus-schubert-winterreise-d-911-03-gefrorne-thranen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/03_Gefror’ne_Thränen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/03_Gefror’ne_Thränen/score.mxl	wir	test	0.0	0.07330316742081448
36	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-12-am-leuchtenden-sommermorgen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/12_Am_leuchtenden_Sommermorgen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/12_Am_leuchtenden_Sommermorgen/score.mxl	wir	test	0.03333333333333333	0.041944444444444444
37	wir-openscore-liedercorpus-wolf-eichendorff-lieder-19-die-nacht	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/19_Die_Nacht/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/19_Die_Nacht/score.mxl	wir	test	0.0	0.1180952380952381
38	wir-openscore-liedercorpus-reichardt-sechs-lieder-von-novalis-op-4-5-noch-ein-bergmannslied	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Sechs_Lieder_von_Novalis,_Op.4/5_Noch_ein_Bergmannslied/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Sechs_Lieder_von_Novalis,_Op.4/5_Noch_ein_Bergmannslied/score.mxl	wir	test	0.0	0.06454545454545454
39	wir-openscore-liedercorpus-hensel-6-lieder-op-9-1-die-ersehnte	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/1_Die_Ersehnte/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/1_Die_Ersehnte/score.mxl	wir	test	0.0	0.02732142857142857
40	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-02-aus-meinen-tranen-spriessen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/02_Aus_meinen_Tränen_sprießen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/02_Aus_meinen_Tränen_sprießen/score.mxl	wir	test	0.0	0.010289855072463768
41	wir-openscore-liedercorpus-schubert-schwanengesang-d-957-05-aufenthalt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/05_Aufenthalt/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/05_Aufenthalt/score.mxl	wir	test	0.02127659574468085	0.028546099290780145
42	wir-openscore-liedercorpus-schubert-op-59-3-du-bist-die-ruh	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Op.59/3_Du_bist_die_Ruh/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Op.59/3_Du_bist_die_Ruh/score.mxl	wir	test	0.012195121951219513	0.024634146341463416
43	wir-openscore-liedercorpus-schubert-schwanengesang-d-957-10-das-fischermadchen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/10_Das_Fischermädchen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/10_Das_Fischermädchen/score.mxl	wir	test	0.013888888888888888	0.013680555555555555
44	wir-bach-wtc-i-24	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/24/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/24/score.mxl	wir	test	0.0	0.09170212765957447
45	wir-bach-wtc-i-15	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/15/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/15/score.mxl	wir	test	0.0	0.1013157894736842
46	wir-bach-wtc-i-8	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/8/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/8/score.mxl	wir	test	0.0	0.03408333333333334
47	wir-bach-wtc-i-3	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/3/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/3/score.mxl	wir	test	0.0	0.06282051282051282
48	wir-bach-chorales-19	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/19/analysis.txt	music21_corpus/music21/corpus/bach/bwv351.mxl	wir	test	0.0	0.031216216216216224
49	wir-bach-chorales-4	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/4/analysis.txt	music21_corpus/music21/corpus/bach/bwv86.6.mxl	wir	test	0.0	0.02024390243902439
50	wir-bach-chorales-10	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/10/analysis.txt	music21_corpus/music21/corpus/bach/bwv38.6.mxl	wir	test	0.0	0.013653846153846154
51	wir-monteverdi-madrigals-book-3-9	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/9/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/9/score.mxl	wir	test	0.014492753623188406	0.0413768115942029
52	wir-monteverdi-madrigals-book-5-7	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/7/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/7/score.mxl	wir	test	0.016666666666666666	0.2921249999999999
53	wir-monteverdi-madrigals-book-5-5	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/5/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/5/score.mxl	wir	test	0.0	0.06380514705882354
54	bps-08-op013-pathetique-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op013(Pathetique)/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_08_01.mxl	bps	validation	0.0	0.140663430420712
55	bps-19-op049-no1-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op049_No1/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_19_01.mxl	bps	validation	0.0	0.06909297052154195
56	bps-29-op106-hammerklavier-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op106(Hammerklavier)/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_29_01.mxl	bps	validation	0.0	0.12237580993520518
57	bps-16-op031-no1-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op031_No1/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_16_01.mxl	bps	validation	0.0030757400999615533	0.14302960399846212
58	bps-26-op081a-les-adieux-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op081a(Les_Adieux)/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_26_01.mxl	bps	validation	0.0	0.288087044534413
59	bps-06-op010-no2-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op010_No2/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_06_01.mxl	bps	validation	0.0	0.12789864029666254
60	bps-20-op049-no2-1	When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op049_No2/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_20_01.mxl	bps	validation	0.0	0.07834016393442624
61	abc-op131-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op131_no14_mov1.mxl	abc	validation	0.008247422680412371	0.7327835051546392
62	abc-op59-no3-1	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No3/1/analysis.txt	AlignedABC/op59_no9_mov1.mxl	abc	validation	0.0	0.22558195926285157
63	abc-op59-no1-4	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No1/4/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no7_mov4.mxl	abc	validation	0.0	0.0785251524390244
64	abc-op18-no1-2	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No1/2/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no1_mov2.mxl	abc	validation	0.004543160020191822	0.09954063604240282
65	abc-op18-no2-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No2/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no2_mov1.mxl	abc	validation	0.0	0.12095381526104418
66	abc-op131-4	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/4/analysis.txt	AlignedABC/op131_no14_mov4.mxl	abc	validation	0.0	0.18385477582846002
67	abc-op132-5	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op132/5/analysis.txt	AlignedABC/op132_no15_mov5.mxl	abc	validation	0.0	0.1728052805280528
68	abc-op18-no6-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No6/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no6_mov1.mxl	abc	validation	0.0	0.1137124060150376
69	abc-op59-no3-3	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No3/3/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no9_mov3.mxl	abc	validation	0.0	0.09953125000000002
70	abc-op18-no3-3	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No3/3/analysis.txt	AlignedABC/op18_no3_mov3.mxl	abc	validation	0.0	0.29562376237623766
71	tavern-mozart-k501-a	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K501/analysis_A.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K501.mxl	tavern	validation	0.0	0.09356682769726248
72	tavern-mozart-k501-b	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K501/analysis_B.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K501.mxl	tavern	validation	0.0	0.08725442834138487
73	tavern-beethoven-woo-64-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_64/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B064.mxl	tavern	validation	0.0	0.1495268138801262
74	tavern-beethoven-woo-64-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_64/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B064.mxl	tavern	validation	0.0	0.2177917981072555
75	tavern-mozart-k455-a	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K455/analysis_A.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K455.mxl	tavern	validation	0.0	0.19421409214092142
76	tavern-mozart-k455-b	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K455/analysis_B.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K455.mxl	tavern	validation	0.0	0.19661246612466124
77	tavern-beethoven-woo-80-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_80/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B080.mxl	tavern	validation	0.0	0.16058551198257082
78	tavern-beethoven-woo-80-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_80/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B080.mxl	tavern	validation	0.0	0.1752750544662309
79	haydnop20-no1-2	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No1/2/analysis.txt	haydn_op20_harm/op20/1/ii/op20n1-02.krn	haydnop20	validation	0.01507537688442211	0.17040201005025127
80	haydnop20-no2-4	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No2/4/analysis.txt	haydn_op20_harm/op20/2/iv/op20n2-04.krn	haydnop20	validation	0.0	0.43603909465020574
81	haydnop20-no3-3	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No3/3/analysis.txt	haydn_op20_harm/op20/3/iii/op20n3-03.krn	haydnop20	validation	0.0	0.04834070796460178
82	haydnop20-no5-2	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No5/2/analysis.txt	haydn_op20_harm/op20/5/ii/op20n5-02.krn	haydnop20	validation	0.0	0.11966666666666666
83	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-13-ich-hab-im-traum-geweinet	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/13_Ich_hab’_im_Traum_geweinet/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/13_Ich_hab’_im_Traum_geweinet/score.mxl	wir	validation	0.0	0.2631004366812227
84	wir-openscore-liedercorpus-hensel-6-lieder-op-9-5-der-maiabend	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/5_Der_Maiabend/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/5_Der_Maiabend/score.mxl	wir	validation	0.0	0.0272
85	wir-openscore-liedercorpus-brahms-6-songs-op-3-3-liebe-und-fruhling-ii	When-in-Rome/Corpus/OpenScore-LiederCorpus/Brahms,_Johannes/6_Songs,_Op.3/3_Liebe_und_Frühling_II/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Brahms,_Johannes/6_Songs,_Op.3/3_Liebe_und_Frühling_II/score.mxl	wir	validation	0.0	0.1322437673130194
86	wir-openscore-liedercorpus-hensel-6-lieder-op-9-3-der-rosenkranz	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/3_Der_Rosenkranz/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/3_Der_Rosenkranz/score.mxl	wir	validation	0.0	0.0477906976744186
87	wir-openscore-liedercorpus-wolf-eichendorff-lieder-08-nachtzauber	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/08_Nachtzauber/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/08_Nachtzauber/score.mxl	wir	validation	0.014925373134328358	0.20731343283582088
88	wir-openscore-liedercorpus-hensel-6-lieder-op-9-4-die-fruhen-graber	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/4_Die_frühen_Gräber/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/4_Die_frühen_Gräber/score.mxl	wir	validation	0.047619047619047616	0.28214285714285714
89	wir-openscore-liedercorpus-mahler-kindertotenlieder-2-nun-seh-ich-wohl-warum-so-dunkle-flammen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Mahler,_Gustav/Kindertotenlieder/2_Nun_seh’_ich_wohl,_warum_so_dunkle_Flammen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Mahler,_Gustav/Kindertotenlieder/2_Nun_seh’_ich_wohl,_warum_so_dunkle_Flammen/score.mxl	wir	validation	0.013513513513513514	0.14219594594594595
90	wir-openscore-liedercorpus-schumann-6-lieder-op-13-3-liebeszauber	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/3_Liebeszauber/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/3_Liebeszauber/score.mxl	wir	validation	0.018475750577367205	0.02406466512702079
91	wir-openscore-liedercorpus-schubert-4-lieder-op-96-1-die-sterne-d-939	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/4_Lieder,_Op.96/1_Die_Sterne,_D.939/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/4_Lieder,_Op.96/1_Die_Sterne,_D.939/score.mxl	wir	validation	0.010638297872340425	0.015026595744680852
92	wir-openscore-liedercorpus-schubert-winterreise-d-911-11-fruhlingstraum	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/11_Frühlingstraum/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/11_Frühlingstraum/score.mxl	wir	validation	0.017429193899782137	0.030108932461873638
93	wir-openscore-liedercorpus-schubert-schwanengesang-d-957-07-abschied	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/07_Abschied/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/07_Abschied/score.mxl	wir	validation	0.011976047904191617	0.0071032934131736525
94	wir-openscore-liedercorpus-schubert-winterreise-d-911-22-muth	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/22_Muth/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/22_Muth/score.mxl	wir	validation	0.0	0.02282608695652174
95	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-01-im-wunderschonen-monat-mai	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/01_Im_wunderschönen_Monat_Mai/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/01_Im_wunderschönen_Monat_Mai/score.mxl	wir	validation	0.0	0.051483253588516756
96	wir-openscore-liedercorpus-schubert-winterreise-d-911-18-der-stuermische-morgen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/18_Der_stuermische_Morgen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/18_Der_stuermische_Morgen/score.mxl	wir	validation	0.0	0.11493421052631578
97	wir-openscore-liedercorpus-schubert-schwanengesang-d-957-13-der-doppelganger	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/13_Der_Doppelgänger/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/13_Der_Doppelgänger/score.mxl	wir	validation	0.015873015873015872	0.043439153439153444
98	wir-bach-wtc-i-7	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/7/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/7/score.mxl	wir	validation	0.0	0.05607142857142858
99	wir-bach-wtc-i-17	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/17/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/17/score.mxl	wir	validation	0.0	0.048863636363636366
100	wir-bach-wtc-i-16	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/16/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/16/score.mxl	wir	validation	0.0	0.054736842105263174
101	wir-bach-wtc-i-11	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/11/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/11/score.mxl	wir	validation	0.0	0.017685185185185186
102	wir-bach-chorales-2	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/2/analysis.txt	music21_corpus/music21/corpus/bach/bwv347.mxl	wir	validation	0.0	0.03018867924528302
103	wir-bach-chorales-14	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/14/analysis.txt	AlignedBachChorales/bwv184.5.mxl	wir	validation	0.0	0.0362280701754386
104	wir-bach-chorales-16	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/16/analysis.txt	music21_corpus/music21/corpus/bach/bwv311.mxl	wir	validation	0.0	0.01601449275362319
105	wir-monteverdi-madrigals-book-3-10	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/10/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/10/score.mxl	wir	validation	0.012048192771084338	0.13090361445783133
106	wir-monteverdi-madrigals-book-3-15	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/15/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/15/score.mxl	wir	validation	0.024390243902439025	0.006463414634146342
107	wir-monteverdi-madrigals-book-3-13	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/13/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/13/score.mxl	wir	validation	0.0	0.06883177570093459
108	bps-02-op002-no2-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op002_No2/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_02_01.mxl	bps	training	0.002973977695167286	0.13998513011152416
109	bps-03-op002-no3-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op002_No3/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_03_01.mxl	bps	training	0.0	0.10608949416342411
110	bps-04-op007-1	When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op007/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_04_01.mxl	bps	training	0.0027624309392265192	0.18744935543278088
111	bps-05-op010-no1-1	When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op010_No1/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_05_01.mxl	bps	training	0.0035211267605633804	0.09044600938967136
112	bps-09-op014-no1-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op014_No1/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_09_01.mxl	bps	training	0.0	0.20796296296296296
113	bps-11-op022-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op022/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_11_01.mxl	bps	training	0.0	0.11661229611041404
114	bps-12-op026-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op026/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_12_01.mxl	bps	training	0.0	0.11390577507598787
115	bps-13-op027-no1-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op027_No1/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_13_01.mxl	bps	training	0.0	0.03481132075471698
116	bps-17-op031-no2-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op031_No2/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_17_01.mxl	bps	training	0.0	0.18157894736842103
117	bps-18-op031-no3-1	When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op031_No3/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_18_01.mxl	bps	training	0.0	0.09461133069828723
118	bps-21-op053-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op053/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_21_01.mxl	bps	training	0.0	0.11971026490066226
119	bps-22-op054-1	When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op054/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_22_01.mxl	bps	training	0.0	0.2061987041036717
120	bps-24-op078-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op078/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_24_01.mxl	bps	training	0.0	0.06308252427184466
121	bps-27-op090-1	When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op090/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_27_01.mxl	bps	training	0.0	0.15182065217391302
122	bps-28-op101-1	When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op101/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_28_01.mxl	bps	training	0.0	0.05715686274509805
123	bps-30-op109-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op109/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_30_01.mxl	bps	training	0.0	0.09918181818181818
124	bps-31-op110-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op110/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_31_01.mxl	bps	training	0.0	0.06964080459770115
125	bps-32-op111-1	AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op111/1/analysis.txt	functional-harmony-micchi/data/BPS/scores/bps_32_01.mxl	bps	training	0.0	0.18875444839857652
126	abc-op131-3	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/3/analysis.txt	AlignedABC/op131_no14_mov3.mxl	abc	training	0.0	1.7470454545454546
127	abc-op95-4	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op95/4/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op95_no11_mov4.mxl	abc	training	0.014247551202137132	0.21913624220837044
128	abc-op132-2	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op132/2/analysis.txt	AlignedABC/op132_no15_mov2.mxl	abc	training	0.004160887656033287	0.24050624133148402
129	abc-op95-2	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op95/2/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op95_no11_mov2.mxl	abc	training	0.0	0.2175520833333333
130	abc-op130-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op130/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op130_no13_mov1.mxl	abc	training	0.0	0.6660334429824561
131	abc-op95-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op95/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op95_no11_mov1.mxl	abc	training	0.0	0.19416390728476823
132	abc-op127-3	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op127/3/analysis.txt	AlignedABC/op127_no12_mov3.mxl	abc	training	0.0	0.20473806752037252
133	abc-op18-no6-2	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No6/2/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no6_mov2.mxl	abc	training	0.0	0.12973101265822787
134	abc-op127-4	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op127/4/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op127_no12_mov4.mxl	abc	training	0.0	0.20169704861111112
135	abc-op130-2	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op130/2/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op130_no13_mov2.mxl	abc	training	0.0	2.8349420849420848
136	abc-op18-no5-3	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No5/3/analysis.txt	AlignedABC/op18_no5_mov3.mxl	abc	training	0.0	0.14122980251346498
137	abc-op59-no1-2	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No1/2/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no7_mov2.mxl	abc	training	0.0	0.24810574229691873
138	abc-op59-no1-3	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No1/3/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no7_mov3.mxl	abc	training	0.0	0.09834586466165414
139	abc-op18-no4-4	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No4/4/analysis.txt	AlignedABC/op18_no4_mov4.mxl	abc	training	0.0	0.10991907514450869
140	abc-op18-no5-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No5/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no5_mov1.mxl	abc	training	0.0	0.12502923976608188
141	abc-op132-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op132/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op132_no15_mov1.mxl	abc	training	0.0	0.17352272727272727
142	abc-op74-2	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op74/2/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op74_no10_mov2.mxl	abc	training	0.0	0.23452662721893489
143	abc-op18-no5-2	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No5/2/analysis.txt	AlignedABC/op18_no5_mov2.mxl	abc	training	0.0	0.18039556962025316
144	abc-op127-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op127/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op127_no12_mov1.mxl	abc	training	0.0	0.18226807228915662
145	abc-op18-no3-2	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No3/2/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no3_mov2.mxl	abc	training	0.0	0.17021523178807946
146	abc-op18-no2-4	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No2/4/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no2_mov4.mxl	abc	training	0.0	0.14345570388349516
147	abc-op131-6	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/6/analysis.txt	AlignedABC/op131_no14_mov6.mxl	abc	training	0.03571428571428571	1.3088690476190474
148	abc-op135-4	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op135/4/analysis.txt	AlignedABC/op135_no16_mov4.mxl	abc	training	0.0	0.5720811744386874
149	abc-op135-3	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op135/3/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op135_no16_mov3.mxl	abc	training	0.0	0.07108024691358025
150	abc-op18-no2-3	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No2/3/analysis.txt	AlignedABC/op18_no2_mov3.mxl	abc	training	0.0	0.2749045801526718
151	abc-op18-no6-4	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No6/4/analysis.txt	AlignedABC/op18_no6_mov4.mxl	abc	training	0.0	0.3466207627118644
152	abc-op59-no3-2	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No3/2/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no9_mov2.mxl	abc	training	0.0	0.7121014492753622
153	abc-op59-no3-4	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No3/4/analysis.txt	AlignedABC/op59_no9_mov4.mxl	abc	training	0.002331002331002331	1.1432954545454546
154	abc-op59-no2-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No2/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no8_mov1.mxl	abc	training	0.0	0.2990581098339719
155	abc-op18-no3-4	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No3/4/analysis.txt	AlignedABC/op18_no3_mov4.mxl	abc	training	0.0026929982046678637	0.19042190305206463
156	abc-op18-no4-1	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No4/1/analysis.txt	AlignedABC/op18_no4_mov1.mxl	abc	training	0.0	0.169615165336374
157	abc-op131-7	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/7/analysis.txt	AlignedABC/op131_no14_mov7.mxl	abc	training	0.005154639175257732	1.4169039948453608
158	abc-op18-no2-2	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No2/2/analysis.txt	AlignedABC/op18_no2_mov2.mxl	abc	training	0.0	0.09705947136563876
159	abc-op130-6	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op130/6/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op130_no13_mov6.mxl	abc	training	0.0	0.5161972891566264
160	abc-op130-5	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op130/5/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op130_no13_mov5.mxl	abc	training	0.0	0.06161616161616161
161	abc-op18-no4-3	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No4/3/analysis.txt	AlignedABC/op18_no4_mov3.mxl	abc	training	0.010169491525423728	1.006779661016949
162	abc-op18-no3-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No3/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no3_mov1.mxl	abc	training	0.0	0.0867020295202952
163	abc-op59-no2-2	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No2/2/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no8_mov2.mxl	abc	training	0.0	0.07210987261146497
164	abc-op59-no2-4	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No2/4/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no8_mov4.mxl	abc	training	0.0	0.23219132029339853
165	abc-op18-no4-2	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No4/2/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no4_mov2.mxl	abc	training	0.0	0.21453384418901658
166	abc-op135-1	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op135/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op135_no16_mov1.mxl	abc	training	0.0	0.20938788659793817
167	abc-op18-no1-4	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No1/4/analysis.txt	AlignedABC/op18_no1_mov4.mxl	abc	training	0.0	0.14818897637795278
168	abc-op132-4	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op132/4/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op132_no15_mov4.mxl	abc	training	0.021739130434782608	0.10512228260869566
169	abc-op18-no5-4	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No5/4/analysis.txt	AlignedABC/op18_no5_mov4.mxl	abc	training	0.0	0.1309737827715356
170	abc-op130-4	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op130/4/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op130_no13_mov4.mxl	abc	training	0.0	0.21468888888888885
171	abc-op131-2	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/2/analysis.txt	AlignedABC/op131_no14_mov2.mxl	abc	training	0.0	0.17852225020990764
172	abc-op74-1	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op74/1/analysis.txt	functional-harmony-micchi/data/Beethoven_4tets/scores/op74_no10_mov1.mxl	abc	training	0.0	0.12998568702290078
173	abc-op132-3	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op132/3/analysis.txt	AlignedABC/op132_no15_mov3.mxl	abc	training	0.0	0.0971987951807229
174	abc-op130-3	AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op130/3/analysis.txt	AlignedABC/op130_no13_mov3.mxl	abc	training	0.0	0.4451278409090909
175	abc-op131-5	When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/5/analysis.txt	AlignedABC/op131_no14_mov5.mxl	abc	training	0.004	0.985655
176	tavern-mozart-k353-a	AlignedWiR/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K353/analysis_A.txt	AlignedTavern/Mozart/K353.mxl	tavern	training	0.0	0.08924690181124881
177	tavern-mozart-k353-b	AlignedWiR/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K353/analysis_B.txt	AlignedTavern/Mozart/K353.mxl	tavern	training	0.0	0.08724499523355578
178	tavern-mozart-k265-a	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K265/analysis_A.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K265.mxl	tavern	training	0.0	0.1447834067547724
179	tavern-mozart-k265-b	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K265/analysis_B.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K265.mxl	tavern	training	0.0	0.12188325991189428
180	tavern-beethoven-woo-73-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_73/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B073.mxl	tavern	training	0.10272952853598015	0.22434243176178664
181	tavern-beethoven-woo-73-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_73/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B073.mxl	tavern	training	0.10272952853598015	0.2045334987593052
182	tavern-beethoven-op34-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/Op34/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/Opus34.mxl	tavern	training	0.0	0.14325023518344307
183	tavern-beethoven-op34-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/Op34/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/Opus34.mxl	tavern	training	0.0	0.143725305738476
184	tavern-mozart-k025-a	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K025/analysis_A.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K025.mxl	tavern	training	0.0	0.18777296360485268
185	tavern-mozart-k025-b	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K025/analysis_B.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K025.mxl	tavern	training	0.0	0.16841421143847488
186	tavern-beethoven-woo-63-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_63/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B063.mxl	tavern	training	0.0	0.05990056818181819
187	tavern-beethoven-woo-63-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_63/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B063.mxl	tavern	training	0.0	0.051526988636363645
188	tavern-beethoven-woo-68-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_68/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B068.mxl	tavern	training	0.0	0.1276427525622255
189	tavern-beethoven-woo-68-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_68/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B068.mxl	tavern	training	0.0	0.13263055148853098
190	tavern-beethoven-woo-66-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_66/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B066.mxl	tavern	training	0.0	0.20576908612260247
191	tavern-beethoven-woo-66-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_66/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B066.mxl	tavern	training	0.0	0.12177510342233923
192	tavern-mozart-k398-a	AlignedWiR/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K398/analysis_A.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K398.mxl	tavern	training	0.0	0.08869963369963371
193	tavern-mozart-k398-b	AlignedWiR/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K398/analysis_B.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K398.mxl	tavern	training	0.0	0.11884615384615385
194	tavern-beethoven-woo-69-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_69/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B069.mxl	tavern	training	0.044180118946474084	0.18134239592183518
195	tavern-beethoven-woo-69-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_69/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B069.mxl	tavern	training	0.044180118946474084	0.21222175021240444
196	tavern-mozart-k573-a	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K573/analysis_A.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K573.mxl	tavern	training	0.0	0.08816403785488959
197	tavern-mozart-k573-b	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K573/analysis_B.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K573.mxl	tavern	training	0.0	0.08809463722397476
198	tavern-beethoven-woo-76-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_76/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B076.mxl	tavern	training	0.0	0.18868147448015124
199	tavern-beethoven-woo-76-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_76/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B076.mxl	tavern	training	0.0	0.18461720226843098
200	tavern-beethoven-woo-72-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_72/analysis_A.txt	AlignedTavern/Beethoven/B072.mxl	tavern	training	0.0	0.11886850152905198
201	tavern-beethoven-woo-72-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_72/analysis_B.txt	AlignedTavern/Beethoven/B072.mxl	tavern	training	0.0	0.1051427115188583
202	tavern-mozart-k613-a	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K613/analysis_A.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K613.mxl	tavern	training	0.0	0.24328586685653256
203	tavern-mozart-k613-b	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K613/analysis_B.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K613.mxl	tavern	training	0.0	0.23892132431470278
204	tavern-beethoven-woo-65-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_65/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B065.mxl	tavern	training	0.0	0.14682119205298014
205	tavern-beethoven-woo-65-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_65/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B065.mxl	tavern	training	0.0	0.1428476821192053
206	tavern-beethoven-op76-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/Op76/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/Opus76.mxl	tavern	training	0.0	0.14569930069930068
207	tavern-beethoven-op76-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/Op76/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/Opus76.mxl	tavern	training	0.0	0.1184965034965035
208	tavern-mozart-k179-a	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K179/analysis_A.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K179.mxl	tavern	training	0.0	0.07674761904761905
209	tavern-mozart-k179-b	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K179/analysis_B.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K179.mxl	tavern	training	0.0	0.0696952380952381
210	tavern-mozart-k354-a	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K354/analysis_A.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K354.mxl	tavern	training	0.0	0.10485335195530725
211	tavern-mozart-k354-b	When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K354/analysis_B.txt	functional-harmony-micchi/data/Tavern/Mozart/scores/K354.mxl	tavern	training	0.0	0.10071229050279328
212	tavern-beethoven-woo-71-a	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_71/analysis_A.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B071.mxl	tavern	training	0.0	0.19537100456621007
213	tavern-beethoven-woo-71-b	When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_71/analysis_B.txt	functional-harmony-micchi/data/Tavern/Beethoven/scores/B071.mxl	tavern	training	0.0	0.18326484018264844
214	haydnop20-no6-3	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No6/3/analysis.txt	haydn_op20_harm/op20/6/iii/op20n6-03.krn	haydnop20	training	0.0	0.13357142857142856
215	haydnop20-no1-1	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No1/1/analysis.txt	haydn_op20_harm/op20/1/i/op20n1-01.krn	haydnop20	training	0.0	0.15910550458715594
216	haydnop20-no4-1	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No4/1/analysis.txt	haydn_op20_harm/op20/4/i/op20n4-01.krn	haydnop20	training	0.009836065573770493	0.17853825136612023
217	haydnop20-no4-3	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No4/3/analysis.txt	haydn_op20_harm/op20/4/iii/op20n4-03.krn	haydnop20	training	0.0	0.09692660550458715
218	haydnop20-no1-3	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No1/3/analysis.txt	haydn_op20_harm/op20/1/iii/op20n1-03.krn	haydnop20	training	0.0	0.13161458333333334
219	haydnop20-no6-2	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No6/2/analysis.txt	haydn_op20_harm/op20/6/ii/op20n6-02.krn	haydnop20	training	0.0	0.1135759493670886
220	haydnop20-no3-1	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No3/1/analysis.txt	haydn_op20_harm/op20/3/i/op20n3-01.krn	haydnop20	training	0.0009250693802035153	0.24731729879740982
221	haydnop20-no5-1	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No5/1/analysis.txt	haydn_op20_harm/op20/5/i/op20n5-01.krn	haydnop20	training	0.0	0.11487189440993789
222	haydnop20-no1-4	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No1/4/analysis.txt	haydn_op20_harm/op20/1/iv/op20n1-04.krn	haydnop20	training	0.0	0.16347893915756628
223	haydnop20-no2-3	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No2/3/analysis.txt	haydn_op20_harm/op20/2/iii/op20n2-03.krn	haydnop20	training	0.023255813953488372	0.4074418604651163
224	haydnop20-no5-4	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No5/4/analysis.txt	haydn_op20_harm/op20/5/iv/op20n5-04.krn	haydnop20	training	0.0	0.11241847826086958
225	haydnop20-no3-2	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No3/2/analysis.txt	haydn_op20_harm/op20/3/ii/op20n3-02.krn	haydnop20	training	0.011320754716981131	0.22732075471698113
226	haydnop20-no4-4	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No4/4/analysis.txt	haydn_op20_harm/op20/4/iv/op20n4-04.krn	haydnop20	training	0.0	0.1270509125840538
227	haydnop20-no2-1	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No2/1/analysis.txt	haydn_op20_harm/op20/2/i/op20n2-01.krn	haydnop20	training	0.0	0.3540871613663133
228	haydnop20-no4-2	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No4/2/analysis.txt	haydn_op20_harm/op20/4/ii/op20n4-02.krn	haydnop20	training	0.016359918200409	0.11934560327198364
229	haydnop20-no6-1	When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No6/1/analysis.txt	haydn_op20_harm/op20/6/i/op20n6-01.krn	haydnop20	training	0.0	1.0443072289156627
230	wir-openscore-liedercorpus-schubert-winterreise-d-911-07-auf-dem-flusse	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/07_Auf_dem_Flusse/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/07_Auf_dem_Flusse/score.mxl	wir	training	0.05405405405405406	0.017195945945945944
231	wir-openscore-liedercorpus-schubert-winterreise-d-911-12-einsamkeit-urspruengliche-fassung	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/12_Einsamkeit_(Urspruengliche_Fassung)/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/12_Einsamkeit_(Urspruengliche_Fassung)/score.mxl	wir	training	0.041666666666666664	0.04645833333333333
232	wir-openscore-liedercorpus-schubert-schwanengesang-d-957-12-am-meer	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/12_Am_Meer/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/12_Am_Meer/score.mxl	wir	training	0.0	0.025722222222222226
233	wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-07-die-wiese	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/07_Die_Wiese/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/07_Die_Wiese/score.mxl	wir	training	0.0	0.11547945205479451
234	wir-openscore-liedercorpus-schubert-winterreise-d-911-16-letzte-hoffnung	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/16_Letzte_Hoffnung/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/16_Letzte_Hoffnung/score.mxl	wir	training	0.0	0.11886925795053004
235	wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-02-der-traurige-wanderer	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/02_Der_traurige_Wanderer/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/02_Der_traurige_Wanderer/score.mxl	wir	training	0.057971014492753624	0.00927536231884058
236	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-15-aus-alten-marchen-winkt-es	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/15_Aus_alten_Märchen_winkt_es/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/15_Aus_alten_Märchen_winkt_es/score.mxl	wir	training	0.18088235294117647	0.14986764705882352
237	wir-openscore-liedercorpus-hensel-6-lieder-op-1-3-warum-sind-denn-die-rosen-so-blass	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/3_Warum_sind_denn_die_Rosen_so_blass/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/3_Warum_sind_denn_die_Rosen_so_blass/score.mxl	wir	training	0.024291497975708502	0.028502024291497976
238	wir-openscore-liedercorpus-schubert-winterreise-d-911-23-die-nebensonnen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/23_Die_Nebensonnen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/23_Die_Nebensonnen/score.mxl	wir	training	0.0	0.01373056994818653
239	wir-openscore-liedercorpus-schubert-winterreise-d-911-05-der-lindenbaum	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/05_Der_Lindenbaum/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/05_Der_Lindenbaum/score.mxl	wir	training	0.0	0.07309959349593495
240	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-11-ein-jungling-liebt-ein-madchen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/11_Ein_Jüngling_liebt_ein_Mädchen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/11_Ein_Jüngling_liebt_ein_Mädchen/score.mxl	wir	training	0.043243243243243246	0.0625945945945946
241	wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-03-die-blume-der-blumen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/03_Die_Blume_der_Blumen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/03_Die_Blume_der_Blumen/score.mxl	wir	training	0.06086956521739131	0.01608695652173913
242	wir-openscore-liedercorpus-wolf-eichendorff-lieder-15-unfall	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/15_Unfall/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/15_Unfall/score.mxl	wir	training	0.0	0.08842975206611571
243	wir-openscore-liedercorpus-schumann-6-lieder-op-13-1-ich-stand-in-dunklen-traumen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/1_Ich_stand_in_dunklen_Träumen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/1_Ich_stand_in_dunklen_Träumen/score.mxl	wir	training	0.0	0.0737837837837838
244	wir-openscore-liedercorpus-hensel-6-lieder-op-1-4-mayenlied	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/4_Mayenlied/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/4_Mayenlied/score.mxl	wir	training	0.06521739130434782	0.08195652173913044
245	wir-openscore-liedercorpus-schumann-frauenliebe-und-leben-op-42-1-seit-ich-ihn-gesehen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Frauenliebe_und_Leben,_Op.42/1_Seit_ich_ihn_gesehen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Frauenliebe_und_Leben,_Op.42/1_Seit_ich_ihn_gesehen/score.mxl	wir	training	0.027777777777777776	0.03638888888888889
246	wir-openscore-liedercorpus-schubert-winterreise-d-911-09-irrlicht	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/09_Irrlicht/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/09_Irrlicht/score.mxl	wir	training	0.0	0.06426356589147288
247	wir-openscore-liedercorpus-schubert-winterreise-d-911-13-die-post	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/13_Die_Post/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/13_Die_Post/score.mxl	wir	training	0.02127659574468085	0.01881205673758865
248	wir-openscore-liedercorpus-chausson-7-melodies-op-2-7-le-colibri	When-in-Rome/Corpus/OpenScore-LiederCorpus/Chausson,_Ernest/7_Mélodies,_Op.2/7_Le_Colibri/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Chausson,_Ernest/7_Mélodies,_Op.2/7_Le_Colibri/score.mxl	wir	training	0.025	0.024900000000000002
249	wir-openscore-liedercorpus-schubert-schwanengesang-d-957-09-ihr-bild	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/09_Ihr_Bild/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/09_Ihr_Bild/score.mxl	wir	training	0.0	0.15291666666666667
250	wir-openscore-liedercorpus-chaminade-amoroso	When-in-Rome/Corpus/OpenScore-LiederCorpus/Chaminade,_Cécile/_/Amoroso/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Chaminade,_Cécile/_/Amoroso/score.mxl	wir	training	0.0	0.0753
251	wir-openscore-liedercorpus-hensel-3-lieder-1-sehnsucht	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/3_Lieder/1_Sehnsucht/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/3_Lieder/1_Sehnsucht/score.mxl	wir	training	0.058823529411764705	0.025073529411764706
252	wir-openscore-liedercorpus-wolf-eichendorff-lieder-13-der-scholar	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/13_Der_Scholar/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/13_Der_Scholar/score.mxl	wir	training	0.0196078431372549	0.09339460784313726
253	wir-openscore-liedercorpus-schubert-winterreise-d-911-14-der-greise-kopf	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/14_Der_greise_Kopf/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/14_Der_greise_Kopf/score.mxl	wir	training	0.0831758034026465	0.09829867674858223
254	wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-09-hier-liegt-ein-spielmann-begraben	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/09_Hier_liegt_ein_Spielmann_begraben/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/09_Hier_liegt_ein_Spielmann_begraben/score.mxl	wir	training	0.09090909090909091	0.014545454545454544
255	wir-openscore-liedercorpus-hensel-6-lieder-op-1-1-schwanenlied	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/1_Schwanenlied/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/1_Schwanenlied/score.mxl	wir	training	0.018518518518518517	0.09768518518518517
256	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-09-das-ist-ein-floten-und-geigen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/09_Das_ist_ein_Flöten_und_Geigen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/09_Das_ist_ein_Flöten_und_Geigen/score.mxl	wir	training	0.04743083003952569	0.051067193675889334
257	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-05-ich-will-meine-seele-tauchen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/05_Ich_will_meine_Seele_tauchen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/05_Ich_will_meine_Seele_tauchen/score.mxl	wir	training	0.0	0.1638418079096045
258	wir-openscore-liedercorpus-wolf-eichendorff-lieder-04-das-standchen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/04_Das_Ständchen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/04_Das_Ständchen/score.mxl	wir	training	0.029850746268656716	0.1693283582089552
259	wir-openscore-liedercorpus-schubert-winterreise-d-911-24-der-leiermann-spatere-fassung	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/24_Der_Leiermann_(Spätere_Fassung)/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/24_Der_Leiermann_(Spätere_Fassung)/score.mxl	wir	training	0.0	0.052240437158469946
260	wir-openscore-liedercorpus-hensel-5-lieder-op-10-3-abendbild	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/3_Abendbild/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/3_Abendbild/score.mxl	wir	training	0.0425531914893617	0.03095744680851064
261	wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-08-kaeuzlein	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/08_Kaeuzlein/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/08_Kaeuzlein/score.mxl	wir	training	0.0759493670886076	0.017088607594936706
262	wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-05-betteley-der-vogel	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/05_Betteley_der_Vögel/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/05_Betteley_der_Vögel/score.mxl	wir	training	0.05	0.016625
263	wir-openscore-liedercorpus-hensel-5-lieder-op-10-5-bergeslust	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/5_Bergeslust/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/5_Bergeslust/score.mxl	wir	training	0.04157043879907621	0.014110854503464202
264	wir-openscore-liedercorpus-schubert-winterreise-d-911-17-im-dorfe	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/17_Im_Dorfe/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/17_Im_Dorfe/score.mxl	wir	training	0.061224489795918366	0.06664965986394557
265	wir-openscore-liedercorpus-coleridge-taylor-oh-the-summer	When-in-Rome/Corpus/OpenScore-LiederCorpus/Coleridge-Taylor,_Samuel/_/Oh,_the_Summer/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Coleridge-Taylor,_Samuel/_/Oh,_the_Summer/score.mxl	wir	training	0.016	0.03064
266	wir-openscore-liedercorpus-schubert-winterreise-d-911-02-die-wetterfahne	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/02_Die_Wetterfahne/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/02_Die_Wetterfahne/score.mxl	wir	training	0.0	0.22360975609756098
267	wir-openscore-liedercorpus-schubert-schwanengesang-d-957-03-fruhlingssehnsucht	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/03_Frühlingssehnsucht/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/03_Frühlingssehnsucht/score.mxl	wir	training	0.0	0.04140776699029126
268	wir-openscore-liedercorpus-lang-6-lieder-op-25-4-lied-immer-sich-rein-kindlich-erfreun	When-in-Rome/Corpus/OpenScore-LiederCorpus/Lang,_Josephine/6_Lieder,_Op.25/4_Lied_(Immer_sich_rein_kindlich_erfreu’n)/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Lang,_Josephine/6_Lieder,_Op.25/4_Lied_(Immer_sich_rein_kindlich_erfreu’n)/score.mxl	wir	training	0.0	0.04195312500000001
269	wir-openscore-liedercorpus-hensel-6-lieder-op-9-2-ferne	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/2_Ferne/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/2_Ferne/score.mxl	wir	training	0.07407407407407407	0.015555555555555555
270	wir-openscore-liedercorpus-schubert-winterreise-d-911-20-der-wegweiser	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/20_Der_Wegweiser/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/20_Der_Wegweiser/score.mxl	wir	training	0.024024024024024024	0.07639639639639641
271	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-14-allnachtlich-im-traume	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/14_Allnächtlich_im_Traume/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/14_Allnächtlich_im_Traume/score.mxl	wir	training	0.0	0.02414012738853503
272	wir-openscore-liedercorpus-schubert-schwanengesang-d-957-14-die-taubenpost	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/14_Die_Taubenpost/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/14_Die_Taubenpost/score.mxl	wir	training	0.0	0.035500000000000004
273	wir-openscore-liedercorpus-schubert-winterreise-d-911-19-tauschung	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/19_Täuschung/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/19_Täuschung/score.mxl	wir	training	0.04633204633204633	0.015714285714285715
274	wir-openscore-liedercorpus-schumann-6-lieder-op-13-6-die-stille-lotosblume	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/6_Die_stille_Lotosblume/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/6_Die_stille_Lotosblume/score.mxl	wir	training	0.0	0.06304964539007091
275	wir-openscore-liedercorpus-schubert-winterreise-d-911-15-die-kraehe	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/15_Die_Kraehe/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/15_Die_Kraehe/score.mxl	wir	training	0.0	0.09363372093023256
276	wir-openscore-liedercorpus-schubert-winterreise-d-911-08-ruckblick	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/08_Rückblick/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/08_Rückblick/score.mxl	wir	training	0.0	0.08487922705314009
277	wir-openscore-liedercorpus-hensel-5-lieder-op-10-4-im-herbste	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/4_Im_Herbste/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/4_Im_Herbste/score.mxl	wir	training	0.0	0.09138157894736842
278	wir-openscore-liedercorpus-franz-6-gesange-op-14-5-liebesfruhling	When-in-Rome/Corpus/OpenScore-LiederCorpus/Franz,_Robert/6_Gesänge,_Op.14/5_Liebesfrühling/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Franz,_Robert/6_Gesänge,_Op.14/5_Liebesfrühling/score.mxl	wir	training	0.0	0.025095238095238094
279	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-03-die-rose-die-lilie	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/03_Die_Rose,_die_Lilie/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/03_Die_Rose,_die_Lilie/score.mxl	wir	training	0.0	0.1900564971751412
280	wir-openscore-liedercorpus-mahler-kindertotenlieder-4-oft-denk-ich-sie-sind-nur-ausgegangen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Mahler,_Gustav/Kindertotenlieder/4_Oft_denk’_ich,_sie_sind_nur_ausgegangen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Mahler,_Gustav/Kindertotenlieder/4_Oft_denk’_ich,_sie_sind_nur_ausgegangen/score.mxl	wir	training	0.0	0.10365319865319865
281	wir-openscore-liedercorpus-hensel-5-lieder-op-10-2-vorwurf	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/2_Vorwurf/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/2_Vorwurf/score.mxl	wir	training	0.0	0.14114795918367345
282	wir-openscore-liedercorpus-schubert-winterreise-d-911-21-das-wirthshaus	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/21_Das_Wirthshaus/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/21_Das_Wirthshaus/score.mxl	wir	training	0.0	0.018528225806451616
283	wir-openscore-liedercorpus-schubert-schwanengesang-d-957-06-in-der-ferne	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/06_In_der_Ferne/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/06_In_der_Ferne/score.mxl	wir	training	0.017094017094017096	0.08678062678062677
284	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-07-ich-grolle-nicht	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/07_Ich_grolle_nicht/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/07_Ich_grolle_nicht/score.mxl	wir	training	0.0	0.015972222222222224
285	wir-openscore-liedercorpus-schubert-schwanengesang-d-957-11-die-stadt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/11_Die_Stadt/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/11_Die_Stadt/score.mxl	wir	training	0.025	0.06891666666666667
286	wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-01-fruhlingsblumen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/01_Frühlingsblumen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/01_Frühlingsblumen/score.mxl	wir	training	0.058823529411764705	0.029117647058823533
287	wir-openscore-liedercorpus-hensel-5-lieder-op-10-1-nach-suden	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/1_Nach_Süden/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/1_Nach_Süden/score.mxl	wir	training	0.06896551724137931	0.015732758620689655
288	wir-openscore-liedercorpus-schubert-winterreise-d-911-10-rast-spatere-fassung	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/10_Rast_(Spätere_Fassung)/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/10_Rast_(Spätere_Fassung)/score.mxl	wir	training	0.0	0.011753731343283582
289	wir-openscore-liedercorpus-wolf-eichendorff-lieder-20-waldmadchen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/20_Waldmädchen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/20_Waldmädchen/score.mxl	wir	training	0.0	0.2067314487632509
290	wir-openscore-liedercorpus-reichardt-zwolf-deutsche-und-italianische-romantische-gesange-10-ida-aus-ariels-offenbarungen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Deutsche_und_Italiänische_Romantische_Gesänge/10_Ida_(aus_Ariels_Offenbarungen)/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Deutsche_und_Italiänische_Romantische_Gesänge/10_Ida_(aus_Ariels_Offenbarungen)/score.mxl	wir	training	0.01818181818181818	0.05345454545454544
291	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-08-und-wusstens-die-blumen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/08_Und_wüssten’s_die_Blumen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/08_Und_wüssten’s_die_Blumen/score.mxl	wir	training	0.026845637583892617	0.1280536912751678
292	wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-04-wachtelwacht	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/04_Wachtelwacht/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/04_Wachtelwacht/score.mxl	wir	training	0.0	0.04935483870967742
293	wir-openscore-liedercorpus-schubert-winterreise-d-911-04-erstarrung	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/04_Erstarrung/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/04_Erstarrung/score.mxl	wir	training	0.01834862385321101	0.039931192660550466
294	wir-openscore-liedercorpus-schubert-schwanengesang-d-957-02-kriegers-ahnung	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/02_Kriegers_Ahnung/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/02_Kriegers_Ahnung/score.mxl	wir	training	0.01507537688442211	0.015609296482412062
295	wir-openscore-liedercorpus-holmes-les-heures-4-lheure-dazur	When-in-Rome/Corpus/OpenScore-LiederCorpus/Holmès,_Augusta_Mary_Anne/Les_Heures/4_L’Heure_d’Azur/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Holmès,_Augusta_Mary_Anne/Les_Heures/4_L’Heure_d’Azur/score.mxl	wir	training	0.04245283018867924	0.028655660377358488
296	wir-openscore-liedercorpus-schubert-winterreise-d-911-06-wasserfluth	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/06_Wasserfluth/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/06_Wasserfluth/score.mxl	wir	training	0.0	0.005416666666666667
297	wir-openscore-liedercorpus-schumann-die-gute-nacht	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/_/Die_gute_Nacht/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/_/Die_gute_Nacht/score.mxl	wir	training	0.01775147928994083	0.049970414201183436
298	wir-openscore-liedercorpus-schumann-dichterliebe-op-48-06-im-rhein-im-heiligen-strome	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/06_Im_Rhein,_im_heiligen_Strome/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/06_Im_Rhein,_im_heiligen_Strome/score.mxl	wir	training	0.0	0.057892473118279573
299	wir-openscore-liedercorpus-schumann-frauenliebe-und-leben-op-42-3-ich-kanns-nicht-fassen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Frauenliebe_und_Leben,_Op.42/3_Ich_kann’s_nicht_fassen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Frauenliebe_und_Leben,_Op.42/3_Ich_kann’s_nicht_fassen/score.mxl	wir	training	0.011583011583011582	0.018803088803088803
300	wir-openscore-liedercorpus-jaell-4-melodies-1-a-toi	When-in-Rome/Corpus/OpenScore-LiederCorpus/Jaëll,_Marie/4_Mélodies/1_À_toi/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Jaëll,_Marie/4_Mélodies/1_À_toi/score.mxl	wir	training	0.05	0.0155
301	wir-openscore-liedercorpus-schumann-lieder-op-12-04-liebst-du-um-schonheit	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/Lieder,_Op.12/04_Liebst_du_um_Schönheit/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/Lieder,_Op.12/04_Liebst_du_um_Schönheit/score.mxl	wir	training	0.024390243902439025	0.07875
302	wir-openscore-liedercorpus-schumann-6-lieder-op-13-2-sie-liebten-sich-beide	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/2_Sie_liebten_sich_beide/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/2_Sie_liebten_sich_beide/score.mxl	wir	training	0.029411764705882353	0.0682843137254902
303	wir-openscore-liedercorpus-hensel-6-lieder-op-1-6-gondellied	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/6_Gondellied/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/6_Gondellied/score.mxl	wir	training	0.07142857142857142	0.024246031746031748
304	wir-openscore-liedercorpus-schubert-winterreise-d-911-01-gute-nacht	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/01_Gute_Nacht/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/01_Gute_Nacht/score.mxl	wir	training	0.009523809523809525	0.011833333333333335
305	wir-openscore-liedercorpus-hensel-6-lieder-op-1-5-morgenstandchen	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/5_Morgenständchen/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/5_Morgenständchen/score.mxl	wir	training	0.0	0.042916666666666665
306	wir-openscore-liedercorpus-brahms-7-lieder-op-48-3-liebesklage-des-madchens	When-in-Rome/Corpus/OpenScore-LiederCorpus/Brahms,_Johannes/7_Lieder,_Op.48/3_Liebesklage_des_Mädchens/analysis.txt	When-in-Rome/Corpus/OpenScore-LiederCorpus/Brahms,_Johannes/7_Lieder,_Op.48/3_Liebesklage_des_Mädchens/score.mxl	wir	training	0.0	0.02108695652173913
307	wir-bach-wtc-i-20	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/20/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/20/score.mxl	wir	training	0.0	0.056309523809523816
308	wir-bach-wtc-i-19	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/19/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/19/score.mxl	wir	training	0.0	0.14416666666666667
309	wir-bach-wtc-i-22	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/22/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/22/score.mxl	wir	training	0.0	0.036458333333333336
310	wir-bach-wtc-i-9	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/9/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/9/score.mxl	wir	training	0.0	0.0403125
311	wir-bach-wtc-i-18	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/18/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/18/score.mxl	wir	training	0.0	0.058333333333333334
312	wir-bach-wtc-i-1	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/1/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/1/score.mxl	wir	training	0.0	0.01542857142857143
313	wir-bach-wtc-i-5	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/5/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/5/score.mxl	wir	training	0.0	0.10335714285714287
314	wir-bach-wtc-i-4	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/4/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/4/score.mxl	wir	training	0.0	0.047008547008547015
315	wir-bach-wtc-i-6	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/6/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/6/score.mxl	wir	training	0.0	0.11514423076923078
316	wir-bach-wtc-i-10	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/10/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/10/score.mxl	wir	training	0.0	0.08445121951219513
317	wir-bach-wtc-i-14	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/14/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/14/score.mxl	wir	training	0.0	0.07671875
318	wir-bach-wtc-i-23	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/23/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/23/score.mxl	wir	training	0.0	0.07144736842105263
319	wir-bach-wtc-i-2	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/2/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/2/score.mxl	wir	training	0.0	0.06927631578947369
320	wir-bach-wtc-i-21	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/21/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/21/score.mxl	wir	training	0.0	0.15775
321	wir-bach-wtc-i-12	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/12/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/12/score.mxl	wir	training	0.0	0.06857954545454546
322	wir-bach-wtc-i-13	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/13/analysis.txt	When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/13/score.mxl	wir	training	0.0	0.06641666666666667
323	wir-bach-chorales-6	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/6/analysis.txt	music21_corpus/music21/corpus/bach/bwv281.mxl	wir	training	0.0	0.004242424242424243
324	wir-bach-chorales-18	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/18/analysis.txt	music21_corpus/music21/corpus/bach/bwv318.mxl	wir	training	0.0	0.024230769230769236
325	wir-bach-chorales-3	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/3/analysis.txt	music21_corpus/music21/corpus/bach/bwv153.1.mxl	wir	training	0.0	0.017926829268292685
326	wir-bach-chorales-9	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/9/analysis.txt	music21_corpus/music21/corpus/bach/bwv248.12-2.mxl	wir	training	0.0	0.06704081632653061
327	wir-bach-chorales-12	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/12/analysis.txt	music21_corpus/music21/corpus/bach/bwv65.2.mxl	wir	training	0.0	0.013469387755102041
328	wir-bach-chorales-7	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/7/analysis.txt	music21_corpus/music21/corpus/bach/bwv17.7.mxl	wir	training	0.0	0.03125
329	wir-bach-chorales-5	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/5/analysis.txt	music21_corpus/music21/corpus/bach/bwv267.mxl	wir	training	0.0	0.03811594202898551
330	wir-bach-chorales-20	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/20/analysis.txt	music21_corpus/music21/corpus/bach/bwv302.mxl	wir	training	0.0	0.032499999999999994
331	wir-bach-chorales-1	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/1/analysis.txt	music21_corpus/music21/corpus/bach/bwv269.mxl	wir	training	0.0	0.012421874999999999
332	wir-bach-chorales-17	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/17/analysis.txt	AlignedBachChorales/bwv145.5.mxl	wir	training	0.0	0.006666666666666666
333	wir-bach-chorales-13	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/13/analysis.txt	music21_corpus/music21/corpus/bach/bwv33.6.mxl	wir	training	0.0	0.025730769230769234
334	wir-bach-chorales-8	When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/8/analysis.txt	music21_corpus/music21/corpus/bach/bwv40.8.mxl	wir	training	0.0	0.0224375
335	wir-monteverdi-madrigals-book-3-14	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/14/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/14/score.mxl	wir	training	0.0	0.02834375
336	wir-monteverdi-madrigals-book-3-6	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/6/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/6/score.mxl	wir	training	0.008130081300813009	0.11668699186991871
337	wir-monteverdi-madrigals-book-3-11	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/11/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/11/score.mxl	wir	training	0.011764705882352941	0.1565
338	wir-monteverdi-madrigals-book-3-19	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/19/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/19/score.mxl	wir	training	0.0	0.18619444444444444
339	wir-monteverdi-madrigals-book-3-8	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/8/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/8/score.mxl	wir	training	0.0	0.09401315789473685
340	wir-monteverdi-madrigals-book-3-3	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/3/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/3/score.mxl	wir	training	0.011111111111111112	0.1486666666666667
341	wir-monteverdi-madrigals-book-4-11	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/11/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/11/score.mxl	wir	training	0.013513513513513514	0.07216216216216217
342	wir-monteverdi-madrigals-book-4-12	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/12/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/12/score.mxl	wir	training	0.0	0.10600746268656716
343	wir-monteverdi-madrigals-book-5-4	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/4/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/4/score.mxl	wir	training	0.0	0.06939024390243903
344	wir-monteverdi-madrigals-book-4-19	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/19/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/19/score.mxl	wir	training	0.01639344262295082	0.048811475409836075
345	wir-monteverdi-madrigals-book-4-13	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/13/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/13/score.mxl	wir	training	0.011235955056179775	0.07949438202247192
346	wir-monteverdi-madrigals-book-4-10	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/10/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/10/score.mxl	wir	training	0.011764705882352941	0.08614705882352941
347	wir-monteverdi-madrigals-book-5-8	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/8/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/8/score.mxl	wir	training	0.010416666666666666	0.09859375
348	wir-monteverdi-madrigals-book-3-1	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/1/analysis.txt	When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/1/score.mxl	wir	training	0.0	0.14224264705882353
349	wir-variations-and-grounds-bach-b-minor-mass-bwv232-crucifixus	When-in-Rome/Corpus/Variations_and_Grounds/Bach,_Johann_Sebastian/B_Minor_mass,_BWV232/Crucifixus/analysis.txt	When-in-Rome/Corpus/Variations_and_Grounds/Bach,_Johann_Sebastian/B_Minor_mass,_BWV232/Crucifixus/score.mxl	wir	training	0.0	0.012452830188679246
350	wir-variations-and-grounds-purcell-sonata-z807	When-in-Rome/Corpus/Variations_and_Grounds/Purcell,_Henry/_/Sonata_Z807/analysis.txt	When-in-Rome/Corpus/Variations_and_Grounds/Purcell,_Henry/_/Sonata_Z807/score.mxl	wir	training	0.0	0.08511904761904761
351	wir-variations-and-grounds-purcell-chacony-z730	When-in-Rome/Corpus/Variations_and_Grounds/Purcell,_Henry/_/Chacony_Z730/analysis.txt	When-in-Rome/Corpus/Variations_and_Grounds/Purcell,_Henry/_/Chacony_Z730/score.mxl	wir	training	0.0	0.06495670995670996
352	wir-orchestral-haydn-symphony-104-1	When-in-Rome/Corpus/Orchestral/Haydn,_Franz_Joseph/Symphony_104/1/analysis.txt	When-in-Rome/Corpus/Orchestral/Haydn,_Franz_Joseph/Symphony_104/1/score.mxl	wir	training	0.013605442176870748	0.06222789115646259
"""


def _annotationScoreHashes():
    for nickname, (annotation, score) in ANNOTATIONSCOREDUPLES.items():
        with open(annotation, "rb") as afd:
            annotationStr = afd.read()
        with open(score, "rb") as sfd:
            scoreStr = sfd.read()
        annotationSha256 = sha256(annotationStr).hexdigest()
        scoreSha256 = sha256(scoreStr).hexdigest()
        annotationSha256GT, scoreSha256GT = hashes[nickname]
        yield (
            nickname,
            annotationSha256GT,
            scoreSha256GT,
            annotationSha256,
            scoreSha256,
        )


class TestDataset(unittest.TestCase):
    def test_dataset_nicknames(self):
        """Checks that the identifiers ('nicknames') haven't changed. """
        self.maxDiff = 20000
        nicknamesGT = tuple(sorted(hashes.keys()))
        nicknames = tuple(sorted(ANNOTATIONSCOREDUPLES.keys()))
        self.assertTupleEqual(nicknamesGT, nicknames)

    def test_dataset_checksums(self):
        """Checks that the annotation,score contents haven't changed. """
        for hashes in _annotationScoreHashes():
            nickname, aGT, sGT, a, s = hashes
            with self.subTest(nickname=nickname):
                self.assertEqual(aGT, a, msg="The annotation hash changed.")
                self.assertEqual(sGT, s, msg="The score hash changed.")

    def test_quality_metrics(self):
        """For files that changed, compare the metrics."""
        for hashes in _annotationScoreHashes():
            nickname, aGT, sGT, a, s = hashes
            annotation, score = ANNOTATIONSCOREDUPLES[nickname]
            with self.subTest(nickname=nickname):
                if aGT == a and sGT == s:
                    # Assume the test will pass
                    continue
                tsvGTF = io.StringIO(datasetTsvGT)
                dfGT = pd.read_csv(tsvGTF, sep="\t")
                misalignmentGT = dfGT[dfGT.file == nickname].misalignmentMean
                qualityGT = dfGT[dfGT.file == nickname].qualityMean
                df = parseAnnotationAndScore(annotation, score)
                misalignment = df.measureMisalignment.mean()
                quality = df.qualitySquaredSum.mean()
                self.assertLessEqual(
                    float(misalignment.round(2)),
                    float(misalignmentGT.round(2)),
                )
                self.assertLessEqual(
                    float(quality.round(2)), float(qualityGT.round(2))
                )
