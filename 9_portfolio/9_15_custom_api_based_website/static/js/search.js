console.log("JS loaded");

const searchForm = document.getElementById("search-form");
const cardsContainer = document.getElementById("brewery-cards");
const noDataMsg = document.getElementById("no-data");

searchForm.addEventListener("submit", function(e){
    e.preventDefault();

    const field = this.field.value;
    const query = this.query.value.trim();

    // 清空舊卡片 & 隱藏 no-data
    cardsContainer.innerHTML = "";
    noDataMsg.style.display = "none";

    if(!query){
        noDataMsg.querySelector("h3").textContent = "Please enter a search term";
        noDataMsg.style.display = "block";
        return;
    }

    console.log("Fetching:", field, query);

    fetch(`/search?field=${encodeURIComponent(field)}&query=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            if(!Array.isArray(data) || data.length === 0){
                noDataMsg.querySelector("h3").textContent = "No Results Found";
                noDataMsg.style.display = "block";
                return;
            }

            data.forEach(b => {
                const card = document.createElement("div");
                card.className = "col-sm-6 col-md-4 col-lg-4";
                card.innerHTML = `
                    <div class="brewery-card p-3 text-center rounded bg-dark text-light border border-warning">
                        <h4>🍺 ${b.name} 🍺</h4>
                        <p>${b.city}, ${b.country}</p>
                        <p class="type fst-italic text-warning">TYPE: ${b.brewery_type}</p>
                        ${b.website_url ? `<p><a href="${b.website_url}" class="text-warning" target="_blank">Website</a></p>` : ""}
                    </div>
                `;
                cardsContainer.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Fetch error:", err);
            noDataMsg.querySelector("h3").textContent = "Error fetching data";
            noDataMsg.style.display = "block";
        });
});
