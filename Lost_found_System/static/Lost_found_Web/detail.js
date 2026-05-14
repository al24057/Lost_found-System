import { Application } from 'https://unpkg.com/@splinetool/runtime@1.9.92/build/runtime.js';

let targetUrl = '';

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    // クラスの付け外しで表示・非表示を切り替える
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

window.toggleSidebar = toggleSidebar;

/* ========================= */
/* Spline 初期化 */
/* ========================= */

const canvas = document.getElementById('canvas3d');

const app = new Application(canvas);

app.load('https://prod.spline.design/aQ2AgVnX5F8V4UIN/scene.splinecode')
.then(() => {

    console.log("Spline読み込み成功");

    /* ========================= */
    /* 対象prefix生成 */
    /* ========================= */

    let prefix = `highlight_${POST_LOCATION}`;

    if (POST_FLOOR) {
        prefix += `_${POST_FLOOR}`;
    }

    console.log(prefix);

    console.log(POST_LOCATION);
    console.log(POST_FLOOR);
    console.log(prefix);

    /* ========================= */
    /* 全highlight取得 */
    /* ========================= */

    const allHighlights = [];

    function searchObjects(obj) {

        /* 名前がある場合 */
        if (obj.name) {

            console.log(obj.name);

            /* highlight_で始まるものを保存 */
            if (obj.name.startsWith('highlight_')) {
                allHighlights.push(obj);
            }
        }

        /* 子オブジェクト再帰探索 */
        if (obj.children) {
            obj.children.forEach(child => {
                searchObjects(child);
            });
        }
    }

    searchObjects(app._scene);

    console.log(allHighlights);

    /* ========================= */
    /* 一旦全部非表示 */
    /* ========================= */

    allHighlights.forEach(obj => {

        obj.visible = false;
        obj.enabled = false;

    });

    /* ========================= */
    /* 対象だけ表示 */
    /* ========================= */

    const targets = allHighlights.filter(obj =>
        obj.name.startsWith(prefix)
    );

    console.log(targets);

    targets.forEach(obj => {

        obj.visible = true;
        obj.enabled = true;

    });

    /* ========================= */
    /* 点滅開始 */
    /* ========================= */

    app.setVariable('show_target', true);

    console.log("Variable ON");

});