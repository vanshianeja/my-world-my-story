// ===== THEME TOGGLE =====
function toggleTheme() {
    document.body.classList.toggle("light");
    const isLight = document.body.classList.contains("light");
    localStorage.setItem("theme", isLight ? "light" : "dark");
    const label = isLight ? "🌙 Dark mode" : "☀️ Light mode";
    document.querySelectorAll(".theme-toggle").forEach(btn => btn.textContent = label);
}

// Apply saved theme on page load
(function() {
    const saved = localStorage.getItem("theme");
    if (saved === "light") {
        document.body.classList.add("light");
        document.querySelectorAll(".theme-toggle").forEach(btn => btn.textContent = "🌙 Dark mode");
    }
})();

// Track selected pills
const selections = {mood: "", genre: "", narrator: "" };

// Track full story so far
let fullStory = "";

// ==== PILL SELECTION ====
function selectPill(pill, group) {
    document.querySelectorAll(`#${group}-pills .pill`)
        .forEach(p => p.classList.remove("selected"));
    pill.classList.add("selected");
    selections[group] = pill.textContent;
}

// ==== ADD CHARACTER ==== 
function addCharacter() {
    const list = document.getElementById("characters-list");
    const card = document.createElement("div");
    card.className = "character-card";
    card.innerHTML = `
    <input type="text" placeholder="Name" class="char-name">
    <input type="text" placeholder="Role (e.g. best friend)" class="char-role">
    <input type="text" placeholder="Traits (e.g. loud, loyal)" class="char-traits">
    <button class="remove-char-btn" onclick="this.parentElement.remove()">✕</button>
    `;
    list.appendChild(card);
}

// ==== COLLECT CHARACTERS ==== 
function getCharacters() {
    const cards = document.querySelectorAll(".character-card");
    const characters = [];
    cards.forEach(card => {
        const name = card.querySelector(".char-name").value.trim();
        const role = card.querySelector(".char-role").value.trim();
        const traits = card.querySelector(".char-traits").value.trim();
        if (name) {
            characters.push({ name, role, traits });
        }
    });
    return characters;
}

// ==== SHOW / HIDE LOADING ====
function showLoading(text) {
    document.getElementById("loading-text").textContent = text;
    document.getElementById("loading").classList.remove("hidden");
}

function hideLoading() {
    document.getElementById("loading").classList.add("hidden")
}

// ==== SWITCH SCREENS ====
function showStoryScreen() {
    document.getElementById("form-screen").classList.remove("active");
    document.getElementById("story-screen").classList.add("active");
    window.scrollTo(0, 0);
}

function goBack() {
    document.getElementById("story-screen").classList.remove("active");
    document.getElementById("form-screen").classList.add("active");
    window.scrollTo(0, 0);
}

// ==== DISPLAY STORY ====
function displayStory(storyText, name, genre, mood) {
    // Split into paragraphs and wrap each in <p> tags
    const paragraphs = storyText.split("\n").filter(p => p.trim() !== "");
    const html = paragraphs.map(p => `<p>${p}</p>`).join("");

    document.getElementById("story-title").textContent = `${name}'s Story`;
    document.getElementById("story-content").innerHTML = html;
    document.getElementById("story-genre-tag").textContent = genre;
    document.getElementById("story-mood-tag").textContent = mood;

    fullStory = storyText;
}

// ==== GENERATE STORY ====
async function generateStory() {
    const name = document.getElementById("name").value.trim();
    const quirk = document.getElementById("quirk").value.trim();
    const mood = selections.mood ||
        document.getElementById("custom-mood").value.trim();
    const genre = selections.genre;
    const narrator = selections.narrator;
    const characters = getCharacters();
    
    // Basic validation
    if (!name) { alert("Please enter your name!"); return; }
    if (!genre) { alert("Please select your genre!"); return; }
    if (!mood) { alert("Please select or describe your mood!"); return; }
    if (!narrator) { alert("Please select a narrator voice!"); return; }

    showLoading("Writing your story...");

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, quirk, characters, mood, genre, narrator })
        });

        const data = await response.json();
        displayStory(data.story, name, genre, mood);
        showStoryScreen();

    } catch (error) {
        alert("Something went wrong. Please try again.");
        console.error(error);
    } finally {
        hideLoading();
    }
}

// ==== SURPRISE ME ====
function surpriseMe() {
    const names = ["Alex", "Maya", "Rohan", "Priya", "Sam"];
    const quirks = [
        "talk to plants when stressed",
        "counts ceiling tiles when nervous",
        "always carries a book they never read"
    ];
    const moods = ["Bittersweet", "Chaotic", "Dreamy", "Tense", "Nostalgic"];
    const genres = ["Romcom", "Suspense", "Fantasy", "Mystery"];
    const narrators = ["Dry & Witty", "Dramatic", "Warm & Gentle"];

    document.getElementById("name").value =
        names[Math.floor(Math.random() * names.length)];
    document.getElementById("quirk").value =
        quirks[Math.floor(Math.random() * quirks.length)];
    
    const randomMood = moods[Math.floor(Math.random() * moods.length)];
    const randomGenre = genres[Math.floor(Math.random() * genres.length)];
    const randomNarrator = narrators[Math.floor(Math.random() * narrators.length)];

    //Auto select pills
    document.querySelectorAll("#mood-pills .pill").forEach(p => {
        if (p.textContent === randomMood) selectPill(p, "mood");
    });

    document.querySelectorAll("#genre-pills .pill").forEach(p => {
        if (p.textContent === randomGenre) selectPill(p, "genre");
    });

    document.querySelectorAll("#narrator-pills .pill").forEach(p => {
        if (p.textContent === randomNarrator) selectPill(p, "narrator");
    });

    // Auto add one character
    addCharacter();

    generateStory();
}

// ==== CONTINUE STORY =====
async function continueStory() {
    const direction = document.getElementById("continue-input").value.trim();
    if (!direction) { alert("Tell me what should happen next!"); return; }

    showLoading("Writing the next chapter...");

    try {
        const response = await fetch("/continue", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify( {
                existing_story: fullStory,
                user_direction: direction
            })
        });

        const data = await response.json();
        const newContent = document.getElementById("story-content");
        const divider = `<hr style="border:none;border-top:1px solid #2a2a35;margin:2rem 0;">`;
        const newParagraphs = data.story.split("\n")
            .filter(p => p.trim() !== "")
            .map(p => `<p>${p}</p>`).join("");
        
        newContent.innerHTML += divider + newParagraphs;
        fullStory += "\n\n" + data.story;
        document.getElementById("continue-input").value = "";
        window.scrollTo(0, document.body.scrollHeight);

    } catch (error) {
        alert("Something went wrong. Please try again.");
    } finally {
        hideLoading();
    }
}

// ==== PLOT TWIST ====
async function plotTwist() {
    showLoading("Twisting the plot...");
    
    try {
        const response = await fetch("/continue", {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify({
                existing_story: fullStory,
                user_direction: "something compleytely unexpected happens - surprise the reader with a plot twist they won't see coming"
            })
        });

    const data = await response.json();
    const newContent = document.getElementById("story-content");
    const divider = `<hr style="border:none;border-top:1px solid #2a2a35;margin:2rem 0;"><p style="color:#5a4fcf;font-size:0.8rem;letter-spacing:0.05em;">⚡ PLOT TWIST</p>`;
    const newParagraphs = data.story.split("\n")
        .filter(p => p.trim() !== "")
        .map(p => `<p>${p}</p>`).join("");

    newContent.innerHTML += divider + newParagraphs;
    fullStory += "\n\n" + data.story;
    window.scrollTo(0, document.body.scrollHeight);
    
    } catch (error) {
        alert("Something went wrong. Please try again.");
    } finally {
        hideLoading();
    }
}

// ==== WORD LOOKUP ====
async function lookupWord() {
    const word = document.getElementById("lookup-input").value.trim();
    if (!word) { alert("Please enter a word!"); return; }

    try {
        const response = await fetch("/lookup", {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify({ word })
        });

        const data = await response.json();
        const resultBox = document.getElementById("lookup-result");

        const synonymsHtml = data.synonyms.length > 0
            ? `<div class="word-synonyms">Synonyms: ${data.synonyms.map(s => `<span>${s}</span>`).join("")}</div>`
            : "";

        resultBox.innerHTML = `
        <div class="word-title">${data.word}</div>
        <div class="word-pos">${data.part_of_speech}</div>
        <div class="word-definition">${data.definition}</div>
        ${synonymsHtml}
        `;

        resultBox.classList.remove("hidden");

    } catch (error) {
        alert("Something went wrong. Please try again.")
    }
}

// ==== SAVE STORY ====
function saveStory() {
    const title = document.getElementById("story-title").textContent;
    const content = document.getElementById("story-content").innerText;
    const blob = new Blob([title + "\n\n" + content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${title}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}