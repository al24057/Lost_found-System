import { Application } from 'https://unpkg.com/@splinetool/runtime@1.9.92/build/runtime.js';

let targetUrl = '';

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

window.toggleSidebar = toggleSidebar;


/* ========================================================= */
/* M1: 3D表示主処理（全体の司令塔）                             */
/* ========================================================= */
function initSplineScene() {
    const canvas = document.getElementById('canvas3d');
    const app = new Application(canvas);

    app.load('https://prod.spline.design/aQ2AgVnX5F8V4UIN/scene.splinecode')
        .then(() => {
            console.log("Spline読み込み成功");
            
            const prefix = generateTargetPrefix();
            const allHighlights = [];
            searchObjects(app._scene, allHighlights);
            controlBlinkTargets(allHighlights, prefix);

            app.setVariable('show_target', true);
            console.log("Variable ON");
        })
        // ★ここから下のエラー処理を追加します！
        .catch((error) => {
            console.error("Spline読み込み失敗:", error); // コンソールにログを出す
            
            // HTMLに用意したエラーメッセージの枠を見えるようにする
            const errorView = document.getElementById('map-error-message');
            if (errorView) {
                errorView.style.display = 'block';
            }
        });
}

/* ========================================================= */
/* M2: 検索条件生成処理                                       */
/* ========================================================= */
function generateTargetPrefix() {
    let prefix = `highlight_${POST_LOCATION}`;
    if (POST_FLOOR) {
        prefix += `_${POST_FLOOR}`;
    }
    return prefix;
}

/* ========================================================= */
/* M3: 3Dオブジェクト探索処理                                 */
/* ========================================================= */
function searchObjects(obj, list) {
    if (obj.name) {
        console.log(obj.name); // 既存のログ出力を残す場合
        if (obj.name.startsWith('highlight_')) {
            list.push(obj);
        }
    }
    if (obj.children) {
        obj.children.forEach(child => searchObjects(child, list));
    }
}

/* ========================================================= */
/* M4: 点滅対象制御処理                                       */
/* ========================================================= */
function controlBlinkTargets(allHighlights, prefix) {
    // 一旦全部非表示
    allHighlights.forEach(obj => {
        obj.visible = false;
        obj.enabled = false;
    });

    // 対象だけ抽出して表示
    const targets = allHighlights.filter(obj => obj.name.startsWith(prefix));
    console.log("ターゲットオブジェクト:", targets);

    targets.forEach(obj => {
        obj.visible = true;
        obj.enabled = true;
    });
}


// 最後に、この画面が開かれた時に司令塔（M1）をスタートさせる
initSplineScene();