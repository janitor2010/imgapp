//import config from '@/config';
//import api from '@/api';


const state = {
    init: false,
    loadings: [],
    showModal: ''
};


const mutations = {

    setItems(state, { dict, response }) {
        state[dict] = response;
    },

    pushItems(state, { dict, response }) {
        if (response.items && response.items.length) {
            if (!state[dict] || !state[dict].items) {
                state[dict] = {
                    items: response.items,
                    total: response.total ? response.total : 0,
                };
            } else {
                response.items.map(el => {
                    state[dict].items.push(el);
                });
                state[dict].total = response.total ? response.total : 0;
            }
        }
    },

    changeItem(state, { dict, item, index }) {
        state[dict].items[index] = item;
    },

    deleteItem(state, {dict, index}) {
        if (index >= 0) {
            if (state[dict].items) {
                state[dict].items.splice(index, 1);
            }
        }
    },

};


const actions = {

    async fetch ({ commit, state }, { dict, params = {} }) {
        state.loadings.push(dict);

        const response = await api.request(config.API_URL + dict + '/', {
            params: params
        });

        if (!params['notState']) {
            if (!params['pushItems'] || !state[dict]) {
                commit('setItems', {
                    dict: dict,
                    response: response
                })
            } else {
                commit('pushItems', {
                    dict: dict,
                    response: response
                })
            }
        }
        state.loadings.slice().map((el, index) => {
            if (el === dict) state.loadings.splice(index, 1);
        });

        return response;
    },

    async clearDict ({ dispatch }, dict ) {
        const response = {
            items: [],
        };
        await dispatch('setItems', { dict, response });
    },

    async submitItem ({ commit, state }, { dict, data }) {
        const response = await api.request(config.API_URL + dict + '/', {
            method: 'PUT',
            data: data,
        });

        // console.log(response);
        if (!data.id) {
            await commit('pushItems', {
                dict: dict,
                response: response
            })
        }
    },

    async submitForm ({ commit, state }, { dict, data }) {
        const response = await api.request('/form/' + dict + '/', {
            method: 'POST',
            data: {item: data},
        });
    },

    async deleteItem({ getters, commit }, {dict, id, prop = 'id'}) {
        let index = getters.indexOf(dict, id, prop);
        commit('deleteItem', {
            dict: dict,
            index: index
        })
    },

    async saveItem({ getters, commit }, { dict, item }) {
        if (!item || !item.id) return ;
        const index = getters.indexOf(dict, item.id);

        if (index === -1) {
            commit('pushItems', {
                dict: dict,
                response: {
                    items: [item]
                }
            })
        } else {
            commit('changeItem', {
                dict: dict,
                item: item,
                index: index,
            })
        }
    },

};


const getters = {

    get: (state, getters) => dict => {
        if (!state[dict] || !state[dict].items || !state[dict].items.length) return [];
        return state[dict].items;
    },

    total: (state, getters) => dict => {
        if (!state[dict] || !state[dict].total) return 0;
        return parseInt(state[dict].total) || 0;
    },

    is: (state, getters) => dict => {
        return state[dict] && state[dict].items;
    },

    length: (state, getters) => dict => {
        return getters.get(dict).length;
    },

    indexOf: (state, getters) => (dict, id, prop = 'id') => {
        if (dict) {
            let list = typeof dict === 'string'
                ? state[dict] && state[dict].items ? state[dict].items : ''
                : dict;
            if (list) {
                id = parseInt(id);
                return list.findIndex(function (el, index, array) {
                    return parseInt(el[prop]) === id;
                });
            }
        }
        return -1;
    },

};

export default {
    namespaced: true,
    actions,
    state,
    mutations,
    getters
}
