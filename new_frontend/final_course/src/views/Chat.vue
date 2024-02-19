<template>
    <div class="container" v-if="auth.getUser.username">
        <button id="expandButton" @click="expandWindow" class="message-show"
            :class="{ 'translated': expanded }">Сообщений</button>
        <div class="content" :class="{ 'expanded': expanded }">

            <button id="expandButton" @click="expandWindow" class="message-hide"
                :class="{ 'hide': expanded === false }">Скрыть</button>

            <div class="message-groupList " v-if="groupList">
                <!-- {{ chatGroup }} -->
                <div v-if="chatGroup" >

                    <form @submit.prevent="chatGroup.createGroup()" class="form-control w-75 m-5">
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault"
                                @change="handleCheck">
                            <label class="form-check-label" for="flexSwitchCheckDefault" v-if="is_private_checkbox">Приватно</label>
                            <label class="form-check-label" for="flexSwitchCheckDefault" v-else>Публично</label>

                        </div>
                        <label class="label-control mt-3" for="group_name_post">Имя группы</label>
                        <div class="input-group">
                            <input type="text" id="group_name_post" class="form-control" v-model="group_name_post"
                                placeholder="Желательно на латинском!">
                            <button class="btn btn-info">Создать</button>
                        </div>

                    </form>
                    <div class="chat-groupList-container">
                        <div class="chat-btn">
                            <button @click="grChange('private')" :class="{ 'color': privateGroupList }">Приватные</button>
                            <button @click="grChange('public')" :class="{ 'color': publicGroupList }">Публичные</button>
                        </div>
                        <div class="chat-grs" v-if="privateGroupList">
                            <div v-if="chatGroup.loading">
                                <h4 class="header-span">Загрузка...</h4>
                            </div>
                            <div class="chat-name" v-if="chatGroup.getPriv" v-for="groups in chatGroup.getPriv"
                                :key="groups.id">
                                <span>{{ groups.name }} </span>
                                <button @click="join(groups.slug)">Присоединиться</button>
                            </div>

                            <div v-else>
                                <h4 class="header-span">Нет приватных групп</h4>
                            </div>


                        </div>
                        <div class="chat-grs" v-else-if="publicGroupList">
                            <div v-if="chatGroup.loading">
                                <h4 class="header-span">Загрузка...</h4>
                            </div>
                            <div class="chat-name" v-if="chatGroup.getPubs" v-for="groups in chatGroup.getPubs"
                                :key="groups.id">
                                <span>{{ groups.name }}</span>
                                <button @click="join(groups.slug)">Присоединиться</button>
                            </div>
                            <div v-else>
                                <h4 class="header-span">Нет публичных групп</h4>
                            </div>

                        </div>
                    </div>

                </div>
                <div v-else class="card w-75 mx-auto my-5 p-3">
                    <span class="card-title">Нет группы!</span>
                    <button class="btn btn-info" @click="CreateForm">Создайте прямо сейчас!</button>

                    <div v-if="showCreateForm" class="my-3">
                        <form @submit.prevent="chatGroup.createGroup()">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault"
                                    @change="handleCheck">
                                <label class="form-check-label" for="flexSwitchCheckDefault">Доступно ли всем?</label>
                            </div>
                            <label class="label-control" for="group_name_post">Имя группы</label>
                            <div class="input-groupList">
                                <input type="text" id="group_name_post" class="form-control" v-model="group_name_post"
                                    placeholder="Желательно на латинском!">
                                <button class="btn btn-info">Создать</button>
                            </div>

                        </form>
                    </div>

                </div>

            </div>
            <div class="messages" v-else>
                <div class="back-to">
                    <button class="btn btn-outline-success" @click="closeWebsocket">Назад к группам</button>
                </div>

                <div class="card p-3 w-75 mx-auto my-5" v-if="chatMess" v-for="m in chatMess.mess" :key="m.timestamp">
                    <!-- {{ chatMess }} -->
                    <span class="card-title"><strong>{{ m.username }}</strong></span>
                    <span class="card-text">{{ m.message }}</span>
                    <p class="card-footer">{{ m.timestamp  }}</p>
                    
                </div>
                <div class="card p-3 w-75 mx-auto my-3" v-else >
                    <span class="card-title">Нет сообщении!</span>
                </div>

                <div class="input-message w-75 mx-auto">
                    <form @submit.prevent="sendMessage">
                        <div class="input-group mt-3">
                            <input type="text" class="form-control" placeholder="Напишите сообщение..."
                                aria-label="Напишите сообщение..." aria-describedby="button-addon2" v-model="messageInput">
                            <button class="btn btn-outline-secondary" id="button-addon2"><i class="bi bi-send"></i></button>
                        </div>
                    </form>
                </div>

            </div>

        </div>
    </div>
</template>

<script>
import { defineComponent, onMounted } from 'vue';
import { useAuthStore } from '@/store/AuthStore';
import { useChatStore, useChatMessage } from '@/store/ChatStore';

export default defineComponent({
    setup() {
        const chatGroup = useChatStore()
        const chatmessage = useChatMessage()
        const authS = useAuthStore()

        onMounted(() => {
            chatGroup.getGroupsOnBack()
        })

        return {
            auth: authS,
            chatGroup: chatGroup,
            chatMess: chatmessage
        }
    },

    data() {
        return {
            expanded: false,
            groupList: true,
            showCreateForm: false,
            group_name_post: null,
            is_private_checkbox: false,
            privateGroupList: false,
            publicGroupList: false,
            socket: null,
            messageInput: '',
            selectedSlug: null,
        }
    },

    async mounted() {
        await this.join(this.selectedSlug)
    },
    methods: {
        expandWindow() {
            this.expanded = !this.expanded;
        },

        grChange(text) {
            if (text === "private") {
                this.privateGroupList = true;
                this.publicGroupList = false;
                // console.log(this.chatGroup)
            } else if (text === "public") {
                this.publicGroupList = true;
                this.privateGroupList = false;
                // console.log(this.chatGroup)

            }
        },

        CreateForm() {
            this.showCreateForm = !this.showCreateForm
        },

        handleCheck() {
            this.is_private_checkbox = !this.is_private_checkbox
            console.log(this.is_private_checkbox)
        },

        



        closeWebsocket() {
            if (this.socket) {
                this.socket.close()
                console.log("websocket closed")
                console.log(this.socket)
            }
        },
        async join(slug) {
            // console.log(slug)

            if (slug) {
                console.log(slug)
                this.selectedSlug = slug;
                const socketUrl = 'ws://' + '127.0.0.1:8000' + '/ws/' + `${slug}/`;
                this.socket = new WebSocket(socketUrl);

                await new Promise((resolve) => {
                    this.socket.addEventListener("open", () => {
                        console.log("WebSocket connection opened");
                        resolve();
                        this.groupList = false;
                    });
                });

                this.socket.addEventListener("message", (event) => {
                    const message = JSON.parse(event.data);
                    // console.log(message); 
                    chatMessage().addMessage(message);
                    console.log(this.chatMess.mess)

                    for (let i in this.chatMess.mess) {
                        console.log(i);
                    }
                    
                });

                this.socket.addEventListener("close", () => {
                    console.log("WebSocket connection closed");
                    this.groupList = true;
                });

                this.socket.addEventListener("error", (error) => {
                    console.error("WebSocket error:", error);
                });


            }

        },

        async sendMessage() {
            if (this.messageInput.trim() !== "") {
                const message = {
                    message: this.messageInput,
                    grSlug: this.selectedSlug,
                    user: this.username
                };

                this.socket.send(JSON.stringify(message));

                this.messageInput = "";
            }
        },

        isoToNormal(isoFormat) {
            const dateObject = new Date(isoFormat);
            const russianDate = dateObject.toLocaleString("ru-RU")
            return russianDate;
        },
    }
})
</script>

<style scoped>
.container {
    position: relative;
    height: 100%;
}

.message-hide {
    position: sticky;
    top: 55%;
    left: 0;
    padding: 10px;
    background-color: #c1e648;
    color: #fff;
    border: none;
    cursor: pointer;
    z-index: 2;
    transform-origin: 0 0;
    transform: rotate(270deg);
}

.message-show {
    transform: translateX(35%) rotate(270deg);
    position: fixed;
    top: 50%;
    right: 0;
    padding: 10px;
    background-color: #c1e648;
    color: #fff;
    border: none;
    cursor: pointer;
    z-index: 2;
    transition: transform 0.5s ease-in-out;
}

.content {
    position: fixed;
    top: 0;
    right: 0;
    width: 0;
    height: 100%;
    background-color: #f2f2f2bb;
    overflow-y: auto;
    transition: width 0.5s ease-in-out;
    z-index: 1;
}

.expanded {
    width: 20%;
    /* z-index: 0; */
}

.translated,
.hide {
    display: none;
}

.back-to {
    width: 100%;
    margin: auto;
}

.input-message {
    position: sticky;
    bottom: 0;
}

.chat-groupList-container {
    background: #fff;
    border-radius: 5px;
    border: none;
    width: 80%;
    margin: 3% auto;
    padding: 2%;
}

.chat-name {
    margin: 0 auto;
    padding-top: 3%;
    padding-bottom: 3%;
    display: flex;
    justify-content: space-between;
    align-items: center;

}

.chat-name button {
    padding: 2%;
    border: none;
    background: #c1e648;
    width: 50%;
    overflow: hidden;
    transition: background 0.3s ease;
}

.chat-name button:hover {
    background: #864c86;
}

.chat-btn {
    display: flex;
    justify-content: center;
    width: 100%;
    overflow: hidden;
}

.chat-btn button:first-child {
    border: none;
    border-radius: 5px 0 0 0;
    padding: 5%;
    background-color: #c1e648;
    width: 50%;

}

.chat-btn button:last-child {
    border: none;
    border-radius: 0 5px 0 0;
    padding: 5%;
    background-color: #c1e648;
    width: 50%;
}

.color {
    background: #864c86 !important;
}

.chat-grs {
    margin: auto;
    border-top: none;
    border-radius: 0 0 5px 5px;
    box-shadow: 0 5px 5px #f2f2f2bb;
    background-color: cornsilk;

}
</style>