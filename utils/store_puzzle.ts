import axios from "axios";
import { JSDOM } from "jsdom";
import { writeFileSync, existsSync, mkdirSync } from "fs";

async function fetchChallengeDescription(day: number): Promise<string> {
  const url = `https://adventofcode.com/2023/day/${day}`;
  try {
    const response = await axios.get(url);
    const dom = new JSDOM(response.data);
    const article = dom.window.document.querySelector(".day-desc");
    return article?.innerHTML || "";
  } catch (error) {
    console.error("Error fetching data:", error);
    return "";
  }
}

function convertToMarkdown(htmlContent: string): string {
  // Simple HTML to Markdown conversion
  // You may use or implement a more sophisticated conversion as needed
  return htmlContent
    .replace(/<h2>(.*?)<\/h2>/g, "## $1\n")
    .replace(/<p>(.*?)<\/p>/g, "$1\n")
    .replace(
      /<ul>(.*?)<\/ul>/gs,
      (match, content) => content.replace(/<li>(.*?)<\/li>/g, "* $1\n") + "\n"
    );
}

async function saveAsMarkdownFile(day: number) {
  const htmlContent = await fetchChallengeDescription(day);
  const markdownContent = convertToMarkdown(htmlContent);
  const title = markdownContent.match(
    /##\s---\s\w+\s(\d+.*?)\s---/m
  ) as string[];
  const formattedTitle = title[1]
    .replaceAll(" ", "_")
    .replace(":", ".")
    .replace(/[^\.\d]\W*?/, "");
  const folderName = `./${formattedTitle}`;
  const fileName = `${folderName}/day_${day}_challenge.md`;

  if (!existsSync(folderName)) {
    mkdirSync(folderName);
  }

  writeFileSync(fileName, markdownContent);
}

const dayArgument = process.argv[2]; // Get the day value from command line argument
const day = Number(dayArgument);

if (!isNaN(day) && day > 0) {
  saveAsMarkdownFile(day);
} else {
  console.error("Please provide a valid day number as an argument.");
}

saveAsMarkdownFile(day);
