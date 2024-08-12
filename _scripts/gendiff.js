const Diff = require('diff');
const fs = require('fs');

function readContract(filePath) {
    return fs.readFileSync(filePath, 'utf8');
}

const contract1895 = readContract('contract1895.md');
const contract1906 = readContract('contract1906.md');
const contract1907 = readContract('contract1907.md');
const contract1910 = readContract('contract1910.md');
const contract1911 = readContract('contract1911.md');
const contract1913 = readContract('contract1913.md');

function generateSideBySideDiffHtml(base, other) {
    const diff = Diff.diffWordsWithSpace(base, other);
    let baseHtml = '<div class="diff-column">';
    let otherHtml = '<div class="diff-column">';
    
    diff.forEach(part => {
        const baseColor = part.removed ? 'red' : 'black';
        const otherColor = part.added ? 'green' : 'black';
        
        if (part.removed) {
            baseHtml += `<span style="color: ${baseColor}; background-color: #ffe6e6;">${part.value}</span>`;
            otherHtml += `<span style="color: ${otherColor}; background-color: #e6ffe6;">&nbsp;</span>`;
        } else if (part.added) {
            baseHtml += `<span style="color: ${baseColor}; background-color: #ffe6e6;">&nbsp;</span>`;
            otherHtml += `<span style="color: ${otherColor}; background-color: #e6ffe6;">${part.value}</span>`;
        } else {
            baseHtml += `<span style="color: ${baseColor}">${part.value}</span>`;
            otherHtml += `<span style="color: ${otherColor}">${part.value}</span>`;
        }
    });
    
    baseHtml += '</div>';
    otherHtml += '</div>';
    
    return `<div class="diff-container">${baseHtml}${otherHtml}</div>`;
}

const diff1895_1906 = generateSideBySideDiffHtml(contract1895, contract1906);
const diff1895_1907 = generateSideBySideDiffHtml(contract1895, contract1907);
const diff1895_1910 = generateSideBySideDiffHtml(contract1895, contract1910);
const diff1895_1911 = generateSideBySideDiffHtml(contract1895, contract1911);
const diff1895_1913 = generateSideBySideDiffHtml(contract1895, contract1913);

fs.writeFileSync('diff1895_1906.html', diff1895_1906);
fs.writeFileSync('diff1895_1907.html', diff1895_1907);
fs.writeFileSync('diff1895_1910.html', diff1895_1910);
fs.writeFileSync('diff1895_1911.html', diff1895_1911);
fs.writeFileSync('diff1895_1913.html', diff1895_1913);
