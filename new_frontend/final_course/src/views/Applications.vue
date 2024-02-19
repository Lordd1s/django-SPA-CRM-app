<template>
    <div v-if="auth.getUser.isMaster">
        <div class="form-container">
            <form @submit.prevent="bidData.sendBid(bid)">
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

            <button class="btn btn-outline-dark mt-3 form-control" @click="bidData.changeShow">Все мои заявки</button>
        </div>

        <div class="text-center" v-if="bidData.showBid">
            <h2 class="h2 text-light">Информация о моих заявках!</h2>
            <h1 class="h1 text-center text-primary" v-if="bidData.getBidData.length === 0">Нет отправленных заявок!</h1>
            <table v-else>
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
                    <tr v-for="bid in bidData.getBidData" :key="bid.id">
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
    <div class="mt-5" v-else-if="auth.getUser.isAdmin || auth.getUser.isStaff">
        <h2 class="h1 mb-5 text-center">Информация о заявках!</h2>
        <h1 class="h1 text-center text-primary" v-if="bidData.getAllData.length === 0">Нет заявок!</h1>

        <section v-else>
            <div class="custom btn-group" role="group" aria-label="Basic mixed styles example">
                <button type="button" @click="type('declined')" class="btn btn-outline-danger">Отклоненные</button>
                <button type="button" @click="type('notViewed')" class="btn btn-outline-warning">На рассмотрении</button>
                <button type="button" @click="type('accepted')" class="btn btn-outline-success">Принятые</button>
            </div>

            <div v-if="bidSol === 'accepted'">
                <div v-for="bid in bidData.getDataAccepted" :key="bid.id" class="bid-list-item">
                    <div class="bid-info">
                        <strong>От кого:</strong> {{ bid._user.username }}<br>
                        <strong>Объект:</strong> {{ bid.object_to }} <br>
                        <strong>Диаметр:</strong> {{ bid.diameter }} мм<br>
                        <strong>Толщина:</strong> SDR {{ bid.thickness }}<br>
                        <strong>Длина:</strong> {{ bid.length }} м.<br>
                        <strong>Тип:</strong> {{ bid.type_of == 'X' ? 'Хлыст' : 'Бухта' }}<br>
                        <h5 class="h5"><strong>Дата отправления:</strong> {{ bid.date_created }}</h5><br>
                        <div class="bid-status" :class="{
                            'text-warning': bid.is_accepted == 2,
                            'text-success': bid.is_accepted == 1,
                            'text-danger': bid.is_accepted != 1 && bid.is_accepted != 2
                        }">
                            {{ bid.is_accepted == 2 ? 'Заявка не решено или не рассмотренный!' : (bid.is_accepted == 1 ?
                                'Заявка принята на обработку!' : 'Заявка отклонено!') }}
                        </div>
                    </div>
                    <div class="bid-actions">
                        <button class="btn btn-success" :disabled="bid.is_accepted != 2"
                            @click="bidData.sendApplicationStatus([bid.id, '1'])">Принять заявку</button>
                        <button class="btn btn-danger" :disabled="bid.is_accepted != 2"
                            @click="bidData.sendApplicationStatus([bid.id, '0'])">Отклонить заявку</button>
                    </div>
                </div>
            </div>

            <div v-else-if="bidSol === 'declined'">
                <div v-for="bid in bidData.getDataDeclined" :key="bid.id" class="bid-list-item">
                    <div class="bid-info">
                        <strong>От кого:</strong> {{ bid._user.username }}<br>
                        <strong>Объект:</strong> {{ bid.object_to }} <br>
                        <strong>Диаметр:</strong> {{ bid.diameter }} мм<br>
                        <strong>Толщина:</strong> SDR {{ bid.thickness }}<br>
                        <strong>Длина:</strong> {{ bid.length }} м.<br>
                        <strong>Тип:</strong> {{ bid.type_of == 'X' ? 'Хлыст' : 'Бухта' }}<br>
                        <h5 class="h5"><strong>Дата отправления:</strong> {{ bid.date_created }}</h5><br>
                        <div class="bid-status" :class="{
                            'text-warning': bid.is_accepted == 2,
                            'text-success': bid.is_accepted == 1,
                            'text-danger': bid.is_accepted != 1 && bid.is_accepted != 2
                        }">
                            {{ bid.is_accepted == 2 ? 'Заявка не решено или не рассмотренный!' : (bid.is_accepted == 1 ?
                                'Заявка принята на обработку!' : 'Заявка отклонено!') }}
                        </div>
                    </div>
                    <div class="bid-actions">
                        <button class="btn btn-success" :disabled="bid.is_accepted != 2"
                            @click="bidData.sendApplicationStatus([bid.id, '1'])">Принять заявку</button>
                        <button class="btn btn-danger" :disabled="bid.is_accepted != 2"
                            @click="bidData.sendApplicationStatus([bid.id, '0'])">Отклонить заявку</button>
                    </div>
                </div>
            </div>

            <div v-else-if="bidSol === 'notViewed'">
                <div v-for="bid in bidData.getDataNotViewed" :key="bid.id" class="bid-list-item">
                    <div class="bid-info">
                        <strong>От кого:</strong> {{ bid._user.username }}<br>
                        <strong>Объект:</strong> {{ bid.object_to }} <br>
                        <strong>Диаметр:</strong> {{ bid.diameter }} мм<br>
                        <strong>Толщина:</strong> SDR {{ bid.thickness }}<br>
                        <strong>Длина:</strong> {{ bid.length }} м.<br>
                        <strong>Тип:</strong> {{ bid.type_of == 'X' ? 'Хлыст' : 'Бухта' }}<br>
                        <h5 class="h5"><strong>Дата отправления:</strong> {{ bid.date_created }}</h5><br>
                        <div class="bid-status" :class="{
                            'text-warning': bid.is_accepted == 2,
                            'text-success': bid.is_accepted == 1,
                            'text-danger': bid.is_accepted != 1 && bid.is_accepted != 2
                        }">
                            {{ bid.is_accepted == 2 ? 'Заявка не решено или не рассмотренный!' : (bid.is_accepted == 1 ?
                                'Заявка принята на обработку!' : 'Заявка отклонено!') }}
                        </div>
                    </div>
                    <div class="bid-actions">
                        <button class="btn btn-success" :disabled="bid.is_accepted != 2"
                            @click="bidData.sendApplicationStatus([bid.id, '1'])">Принять заявку</button>
                        <button class="btn btn-danger" :disabled="bid.is_accepted != 2"
                            @click="bidData.sendApplicationStatus([bid.id, '0'])">Отклонить заявку</button>
                    </div>
                </div>
            </div>

            <div v-else>
                <div v-for="bid in bidData.getAllData" :key="bid.id" class="bid-list-item">
                    <div class="bid-info">
                        <strong>От кого:</strong> {{ bid._user.username }}<br>
                        <strong>Объект:</strong> {{ bid.object_to }} <br>
                        <strong>Диаметр:</strong> {{ bid.diameter }} мм<br>
                        <strong>Толщина:</strong> SDR {{ bid.thickness }}<br>
                        <strong>Длина:</strong> {{ bid.length }} м.<br>
                        <strong>Тип:</strong> {{ bid.type_of == 'X' ? 'Хлыст' : 'Бухта' }}<br>
                        <h5 class="h5"><strong>Дата отправления:</strong> {{ bid.date_created }}</h5><br>
                        <div class="bid-status" :class="{
                            'text-warning': bid.is_accepted == 2,
                            'text-success': bid.is_accepted == 1,
                            'text-danger': bid.is_accepted != 1 && bid.is_accepted != 2
                        }">
                            {{ bid.is_accepted == 2 ? 'Заявка не решено или не рассмотренный!' : (bid.is_accepted == 1 ?
                                'Заявка принята на обработку!' : 'Заявка отклонено!') }}
                        </div>
                    </div>
                    <div class="bid-actions">
                        <button class="btn btn-success" :disabled="bid.is_accepted != 2"
                            @click="bidData.sendApplicationStatus([bid.id, '1'])">Принять заявку</button>
                        <button class="btn btn-danger" :disabled="bid.is_accepted != 2"
                            @click="bidData.sendApplicationStatus([bid.id, '0'])">Отклонить заявку</button>
                    </div>
                </div>
            </div>
        </section>



    </div>
</template>

<script>
import { defineComponent, onMounted } from 'vue';
import { useAuthStore } from '@/store/AuthStore';
import { useBidStore } from '@/store/ApplicationStore';

export default defineComponent({
    setup() {
        const authStores = useAuthStore()
        const bidStore = useBidStore()

        onMounted(() => {
            if (authStores.getUser.isAdmin || authStores.getUser.isStaff) {
                bidStore.getApplications()
                console.log('админ')
            } else {
                bidStore.getBid()
                console.log('мастер')
            }

        })
        return {
            auth: authStores,
            bidData: bidStore
        }
    },
    data() {
        return {
            bid: {
                diameter: null,
                thickness: null,
                type_of: null,
                length: null,
                object_to: null
            },
            bidSol: null,

        }
    },

    methods: {
        type(t) {
            switch (t) {
                case 'accepted':
                    this.bidSol = 'accepted'
                    break;
                case 'declined':
                    this.bidSol = 'declined'
                    break;
                case 'notViewed':
                    this.bidSol = 'notViewed'
                default:
                    break;
            }
        }
    },
})
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

.custom {
    max-width: 40%;
    margin: 0 auto;
    padding: 15px;
    background-color: #ebebeb;
    display: flex !important;
    box-shadow: 0 0 5px #fff;

}
</style>
