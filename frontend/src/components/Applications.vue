<template>
    <div v-if="isMaster">
        <div class="form-container">
            <form @submit.prevent="sendBid">
                <div class="form-group">
                    <label for="diameter">Диаметр (мм):</label>
                    <input type="number" min="32" id="diameter" name="diameter" required v-model="bid.diameter">
                </div>

                <div class="form-group">
                    <label for="thickness">Толщина (SDR):</label>
                    <input type="number" min="7" id="thickness" name="thickness" required v-model="bid.thickness">
                </div>

                <div class="form-group">
                    <label for="length">Длина (м):</label>
                    <input type="number" min="0" id="length" name="length" required v-model="bid.length">
                </div>

                <div class="form-group">
                    <label for="object">Объект:</label>
                    <input type="text" id="object" required v-model="bid.object_to">
                </div>

                <div class="form-group">
                    <label for="type">Тип:</label>
                    <div class="select-wrapper">
                        <select id="type" name="type" required v-model="bid.type_of">
                            <option value="X">Хлыст</option>
                            <option value="B" :disabled="bid.diameter > 90">Бухта</option>
                        </select>
                        <div class="select-arrow">&#9660;</div>
                    </div>
                </div>
                <button class="btn btn-outline-dark form-control">Отправить</button>
            </form>

            <button class="btn btn-outline-dark mt-3 form-control" @click="getBid">Все мои заявки</button>
        </div>

        <div class="text-center" v-if="showBid">
            <h2 class="h2 text-light">Информация о моих заявках!</h2>
            <table>
                <thead>
                    <tr>
                        <th>Диаметр</th>
                        <th>Толщина</th>
                        <th>Длина</th>
                        <th>Тип</th>
                        <th>Дата отправления</th>
                        <th>Решение</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="bid in bidData" :key="bid.id">
                        <td>{{ bid.diameter }} мм</td>
                        <td>SDR {{ bid.thickness }}</td>
                        <td>{{ bid.length }} м.</td>
                        <td v-if="bid.type_of == 'X'">Хлыст</td>
                        <td v-else="bid.type_of == 'B'">Бухта</td>
                        <td>{{ bid.date_created }}</td>
                        <td class="text-warning" v-if="bid.is_accepted == 2">Заявка не решено или не расмотренный</td>
                        <td class="text-success" v-else-if="bid.is_accepted == 1">Заявка принята</td>
                        <td class="text-danger" v-else>Заявка отклонено</td>

                    </tr>
                </tbody>
            </table>
        </div>

    </div>
    <div class="mt-5" v-else-if="isAdmin || isStaff">
        <h2 class="h1 mb-5 text-center">Информация о заявках!</h2>
        <div v-for="bid in data" :key="bid.id" class="bid-list-item">
            <div class="bid-info">
                <strong>От кого:</strong> {{ bid._user.username }}<br>
                <strong>Объект:</strong> {{ bid.object_to }} <br>
                <strong>Диаметр:</strong> {{ bid.diameter }} мм<br>
                <strong>Толщина:</strong> SDR {{ bid.thickness }}<br>
                <strong>Длина:</strong> {{ bid.length }} м.<br>
                <strong>Тип:</strong> {{ bid.type_of == 'X' ? 'Хлыст' : 'Бухта' }}<br>
                <strong>Дата отправления:</strong> {{ bid.date_created }}<br>
                <div class="bid-status" :class="{
                    'text-warning': bid.is_accepted == 2,
                    'text-success': bid.is_accepted == 1,
                    'text-danger': bid.is_accepted != 1 && bid.is_accepted != 2
                }">
                    {{ bid.is_accepted == 2 ? 'Заявка не решено или не рассмотренный!' : (bid.is_accepted == 1 ? 'Заявка принята на обработку!' : 'Заявка отклонено!') }}
                </div>
            </div>
            <div class="bid-actions">
                <button class="btn btn-success" :disabled="bid.is_accepted != 2"
                    @click="sendApplicationStatus([bid.id, '1'])">Принять заявку</button>
                <button class="btn btn-danger" :disabled="bid.is_accepted != 2"
                    @click="sendApplicationStatus([bid.id, '0'])">Отклонить заявку</button>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios';
// import { defineComponent } from 'vue';
import { authStore } from '@/store/store';

export default {
    setup() {
        const authStores = authStore()

        return { 
            isAdmin: authStores.isAdmin,
            isStaff: authStores.isStaff, 
            isMaster: authStores.isMaster,
         }
    },
    data() {
        return {
            data: null,
            bid: {
                diameter: null,
                thickness: null,
                type_of: null,
                length: null,
                object_to: null
            },
            bidData: null,
            showBid: false,
        }
    },

    async mounted() {
        await this.getApplications()
    },

    methods: {
        async getApplications() {
            if (this.isAdmin || this.isStaff) {
                try {
                    const rs = await axios.get('http://127.0.0.1:8000/applications/solution',
                        {
                            headers: {
                                Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                            }
                        }
                    )
                    this.data = rs.data;
                } catch (error) {
                    console.error(error)
                }
            } else if (this.isMaster) {
                console.log('Доступ только высшим начальникам!')
                return null;
            }
        },

        async sendApplicationStatus(st) {
            const [pk, status] = st
            try {
                await axios.patch(`http://127.0.0.1:8000/applications/solution?status=${status}&pk=${pk}`, {},
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    })
                window.location.reload()
            } catch (error) {
                console.error(error)
            }
        },

        async sendBid() {
            try {
                await axios.post('http://127.0.0.1:8000/application/', this.bid,
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    })
                alert('Заявка успешно отправлена!')
                this.bid.diameter = null;
                this.bid.thickness = null;
                this.bid.type_of = null;
                this.bid.length = null;
                this.bid.object_to = null;
            } catch (error) {
                console.error(error)
                alert(error)
            }
        },

        async getBid() {
            this.showBid = true;
            try {
                const res = await axios.get('http://127.0.0.1:8000/application/',
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    })
                this.bidData = res.data
                console.log(res.data)
            } catch (error) {
                console.error(error)
            }
        }
    }
}
</script>

<style scoped>
.form-container {
    margin: 2% auto;
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    max-width: 30%;
}

.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #333;
}

select,
input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-bottom: 10px;
}

.select-wrapper {
    position: relative;
}

select {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    padding-right: 30px;
    cursor: pointer;
    background-color: #fff;
}

.select-arrow {
    position: absolute;
    top: 50%;
    right: 10px;
    transform: translateY(-50%);
}

table {
    border-collapse: collapse;
    width: 70%;
    margin: 0 auto;
    margin-bottom: 20px;
}

th,
td {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

th {
    background-color: #f2f2f2;
}

tr:nth-child(even) {
    background-color: #ebebeb;
}

tr:nth-child(odd) {
    background-color: #e2e0e0;
}

.bid-list-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: none;
    background: #ebebeb;
    border-radius: 5px;
    box-shadow: 0 0 5px #fff;
    padding: 15px;
    margin: 1% auto;
    max-width: 40%;
}

.bid-info {
    flex: 1;
    margin-right: 10px;
}

.bid-status {
    margin-top: 10px;
    font-weight: bold;
}

.bid-actions button {
    margin-left: 10px;
}

</style>