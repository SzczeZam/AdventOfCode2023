"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const axios_1 = __importDefault(require("axios"));
const jsdom_1 = require("jsdom");
const fs_1 = require("fs");
function fetchChallengeDescription(day) {
    return __awaiter(this, void 0, void 0, function* () {
        const url = `https://adventofcode.com/2023/day/${day}`;
        try {
            const response = yield axios_1.default.get(url);
            const dom = new jsdom_1.JSDOM(response.data);
            const article = dom.window.document.querySelector(".day-desc");
            return (article === null || article === void 0 ? void 0 : article.innerHTML) || "";
        }
        catch (error) {
            console.error("Error fetching data:", error);
            return "";
        }
    });
}
function convertToMarkdown(htmlContent) {
    // Simple HTML to Markdown conversion
    // You may use or implement a more sophisticated conversion as needed
    return htmlContent
        .replace(/<h2>(.*?)<\/h2>/g, "## $1\n")
        .replace(/<p>(.*?)<\/p>/g, "$1\n")
        .replace(/<ul>(.*?)<\/ul>/gs, (match, content) => content.replace(/<li>(.*?)<\/li>/g, "* $1\n") + "\n");
}
function saveAsMarkdownFile(day) {
    return __awaiter(this, void 0, void 0, function* () {
        const htmlContent = yield fetchChallengeDescription(day);
        const markdownContent = convertToMarkdown(htmlContent);
        const title = markdownContent.match(/##\s---\s\w+\s(\d+.*?)\s---/m);
        const formattedTitle = title[1]
            .replaceAll(" ", "_")
            .replace(":", ".")
            .replace(/[^\.\d]\W*?/, "");
        const folderName = `./${formattedTitle}`;
        const fileName = `${folderName}/day_${day}_challenge.md`;
        if (!(0, fs_1.existsSync)(folderName)) {
            (0, fs_1.mkdirSync)(folderName);
        }
        (0, fs_1.writeFileSync)(fileName, markdownContent);
    });
}
const dayArgument = process.argv[2]; // Get the day value from command line argument
const day = Number(dayArgument);
if (!isNaN(day) && day > 0) {
    saveAsMarkdownFile(day);
}
else {
    console.error("Please provide a valid day number as an argument.");
}
saveAsMarkdownFile(day);
