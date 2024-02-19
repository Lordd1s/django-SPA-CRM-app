import { defineStore } from "pinia";
import axios from "axios";
import { ref } from "vue";
import router from "@/router";

export const useVacancyStore = defineStore(
    "useVacancyStore",
    {
        state: () => ({
            loading: false,
            error: ref(null),
            message: '',
            vacancyData: {},
            showForm: false,
            showVac: true,
        }),

        actions: {
            async Vacancy() {
                this.loading = true;
                try {
                    const response = await axios.get("http://127.0.0.1:8000/vacancy/");
                    // console.log(response);
                    if (response.status === 200) {
                       this.vacancyData = response.data;
                    }
                    
                    // console.log(this.vacancy)
                } catch (error) {
                    this.error = error;
                    console.error(error);
    
                } finally {
                    this.loading = false;
                }
    
            },

            async deleteVacancy(vacancy) {
                // console.log(vacancy)
                try {
                    await axios.delete(`http://127.0.0.1:8000/cud_vacancy/${vacancy.id}/`,
                        {
                            headers: {
                                Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                            }
                        })
                    this.message = 'Success'
                    this.vacancyData = this.vacancyData.filter(item => item.id !== vacancy.id);
                } catch (error) {
                    this.error = error;
                    console.error(error);
                    
                }
            },

            async updVac(changedVacancy) {
                try {
                    await axios.put(`http://127.0.0.1:8000/cud_vacancy/${changedVacancy.id}/`, changedVacancy,
                        {
                            headers: {
                                Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                            }
                        })
                    this.message = 'Updated'
                } catch (error) {
                    this.error = error;
                    console.error(error)
                } finally {
                    setInterval(() => {
                        this.message = ''
                    }, 5000)
                }
            },
        },

        getters: {
            getVacancyData() {
                return this.vacancyData
            }
        },
    }
)

export const useVacancyCreate = defineStore(
    'useVacancyCreate',
    {
        state: () => ({
            loading: false,
            error: ref(null),
        }),

        actions: {
            async createVacancy(vacancy) {
                this.loading = true;
                try {
                    const request = await axios.post(`http://127.0.0.1:8000/cud_vacancy/' '/`, vacancy, 
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    })
                    if (request.status === 201) {
                      alert('Вакансия успешно создана');  
                    } else if (request.status === 400) {
                        alert('Заполните все поля!')
                        this.error = 'Заполните все поля!'
                    }
                    
                    router.push({name: 'Vacancy'});
                } catch (error) {
                    console.error(error);
                    this.error = error;
                } finally {
                    this.loading = false;
                }
            }
        }
    }
)