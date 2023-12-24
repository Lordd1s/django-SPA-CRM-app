<template>
    <div class="crypto-prices-container bg-dark">
        <div class="crypto-prices-header">
            <h1 class="h1 text-center">Цены на криптовалюты!</h1>
        </div>
        <div class="crypto-prices-table">
            <table class="table table-striped">
                <thead>
                    <tr class="table-warning">
                        <th>Название</th>
                        <th>Цена USD</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="crypto.data.length === 0">
                        <td colspan="2" class="text-center">
                            Загрузка данных...
                            <div class="spinner-border spinner-border-sm" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </td>
                    </tr>
                    <tr v-else v-for="item in crypto.data" :key="item.rank">
                        <td>{{ item.symbol }}</td>
                        <td>$ {{ item.priceUsd }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            crypto: { data: [] }
        }
    },
    async mounted() {
        await this.getCrypto();
    },

    methods: {
        async getCrypto() {
            try {
                const response = await axios.get('https://api.coincap.io/v2/assets');
                this.crypto = response.data;
            } catch (error) {
                console.log(error);
            }
        }
    }
}
</script>

<style scoped>
.crypto-prices-container {
    max-width: 800px;
    margin: 2% auto;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    /* Добавлено для обрезания углов таблицы */
}

.crypto-prices-header {
    margin-bottom: 20px;
}

.crypto-prices-table {
    overflow-x: auto;
}

.table {
    border-collapse: collapse;
    width: 100%;
    margin-top: 20px;
}

.table th,
.table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #dee2e6;
}

.table-warning {
    background-color: #ffc107;
    color: #212529;
}

.spinner-border {
    margin-left: 10px;
    vertical-align: text-bottom;
}

.h1 {
    font-size: 72px;
    background: linear-gradient(60deg, #c1e648, #864c86, #ffffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
@media screen and (max-width: 768px)  {
    .h1 {
        font-size: 1.5rem;
    }

    .crypto-prices-container {
        width: 95%;
    }
}
</style>