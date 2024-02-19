<template>
    <div class="text-center" v-if="news == null">
        <h1 class="h1 mt-5">Загрузка</h1>
        <div class="loader"></div>
    </div>
    <div class="container-sm" v-else>
        <nav aria-label="Page navigation example" class="my-3">
            <ul class="pagination justify-content-center">
                <li class="page-item" :class="{ 'disabled': currentPage === 1 }">
                    <a class="page-link" @click="changePage(currentPage - 1)" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                </li>
                <li class="page-item" v-for="page in pages" :key="page" :class="{ 'active': currentPage === page }">
                    <a class="page-link" @click="changePage(page)">{{ page }}</a>
                </li>
                <li class="page-item" :class="{ 'disabled': currentPage === totalPages }">
                    <a class="page-link" @click="changePage(currentPage + 1)" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                </li>
            </ul>
        </nav>
        <div class="news-cards-container">
            <div class="news-card" v-for="nu in paginatedNews" :key="nu.publishedAt">
                <div class="news-image" v-if="nu.urlToImage">
                    <img :src="nu.urlToImage" alt="News Image">
                </div>
                <div class="news-details">
                    <span class="news-author">Автор {{ nu.author }}</span>
                    <span>Источник {{ nu.source.name }}</span>
                    <h2 class="news-title">{{ nu.title }}</h2>
                    <p class="news-description">{{ nu.description }}</p>
                    <a :href="nu.url" target="_blank" class="read-more">Подробнее</a>
                    <span class="news-date">Дата публикации {{ this.normalDate(nu.publishedAt) }}</span>
                </div>
            </div>
        </div>

        <nav aria-label="Page navigation example">
            <ul class="pagination justify-content-center">
                <li class="page-item" :class="{ 'disabled': currentPage === 1 }">
                    <a class="page-link" @click="changePage(currentPage - 1)" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                </li>
                <li class="page-item" v-for="page in pages" :key="page" :class="{ 'active': currentPage === page }">
                    <a class="page-link" @click="changePage(page)">{{ page }}</a>
                </li>
                <li class="page-item" :class="{ 'disabled': currentPage === totalPages }">
                    <a class="page-link" @click="changePage(currentPage + 1)" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            news: null,
            currentPage: 1,
            itemsPerPage: 8,
        }
    },
    async mounted() {
        await this.getNews()
    },
    methods: {
        async getNews() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/newsletter/')
                // console.log(response)
                this.news = response.data.articles
                // console.log(this.news)
            } catch (error) {
                console.error(error)
            }
        },

        normalDate(datestring) {
            const toFormat = new Date(datestring)
            const formatted = toFormat.toLocaleString('ru-RU')
            return formatted
        },

        changePage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
            }
        },
    },
    computed: {
        totalPages() {
            return Math.ceil(this.news.length / this.itemsPerPage);
        },
        paginatedNews() {
            const startIndex = (this.currentPage - 1) * this.itemsPerPage;
            const endIndex = startIndex + this.itemsPerPage;
            return this.news.slice(startIndex, endIndex);
        },
        pages() {
            return Array.from({ length: this.totalPages }, (_, index) => index + 1);
        },
    },
}
</script>

<style scoped>
.news-cards-container {
    display: grid;
    grid-auto-columns: auto;
    grid-auto-rows: auto;
    gap: 20px;
    padding: 20px;

}

.news-card {
    background-color: #fff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    overflow: hidden;
    transition: transform 0.2s ease-in-out;
}

.news-card:hover {
    transform: scale(1.02);
}

.news-image img {
    width: 100%;
    height: auto;
    border-bottom: 2px solid #ddd;
    border-radius: 10px 10px 0 0;
}

.news-details {
    padding: 20px;
}

.news-author {
    display: block;
    font-size: 14px;
    color: #777;
}

.news-title {
    font-size: 24px;
    margin: 10px 0;
    color: #333;
}

.news-description {
    font-size: 16px;
    color: #555;
}

.read-more {
    display: inline-block;
    padding: 8px 16px;
    background-color: #007BFF;
    color: #fff;
    text-decoration: none;
    border-radius: 5px;
    margin-top: 10px;
    transition: background-color 0.3s ease;
}

.read-more:hover {
    background-color: #0056b3;
}

.news-date {
    display: block;
    font-size: 14px;
    color: #888;
    margin-top: 10px;
}

@media screen and (max-width: 600px) {
    .news-cards-container {
        grid-template-columns: 1fr;
    }
}

.loader {
    width: 100px;
    height: 100px;
    margin: 2% auto;
    position: relative;
}

.loader:before {
    content: '';
    width: 48px;
    height: 5px;
    background: #000;
    opacity: 0.25;
    position: absolute;
    top: 60px;
    left: 0;
    border-radius: 50%;
    animation: shadow 0.5s linear infinite;
}

.loader:after {
    content: '';
    width: 100%;
    height: 100%;
    background: #fff;
    animation: bxSpin 0.5s linear infinite;
    position: absolute;
    top: 0;
    left: 0;
    border-radius: 4px;
}

@keyframes bxSpin {
    17% {
        border-bottom-right-radius: 3px;
    }

    25% {
        transform: translateY(9px) rotate(22.5deg);
    }

    50% {
        transform: translateY(18px) scale(1, .9) rotate(45deg);
        border-bottom-right-radius: 40px;
    }

    75% {
        transform: translateY(9px) rotate(67.5deg);
    }

    100% {
        transform: translateY(0) rotate(90deg);
    }
}

@keyframes shadow {

    0%,
    100% {
        transform: scale(1, 1);
    }

    50% {
        transform: scale(1.2, 1);
    }
}
</style>