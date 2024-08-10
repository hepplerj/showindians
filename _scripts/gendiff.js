const Diff = require('diff');
const fs = require('fs');

function readContract(filePath) {
    return fs.readFileSync(filePath, 'utf8');
}

const contract1906 = readContract('contract1906.txt');
const contract1907 = readContract('contract1907.txt');
const contract1911 = readContract('contract1911.txt');

function generateDiffHtml(base, other) {
    const diff = Diff.diffWords(base, other);
    let html = '<div class="diff">';
    diff.forEach(part => {
        const color = part.added ? 'green' : part.removed ? 'red' : 'black';
        const span = `<span style="color: ${color}">${part.value}</span>`;
        html += span;
    });
    html += '</div>';
    return html;
}
