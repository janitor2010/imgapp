//import api from '@f/api';

export const openModal = ({state, commit}, { name, what }) => {
    commit('set', {
        name: 'showModal',
        value: name
    })
    commit('set', {
        name: 'modalFormWhat',
        value: what
    })
};

export const saveToState = ({commit}, { name, value }) => {
    commit('set', {
        name: name,
        value: value
    })
};

export const updateForm = ({commit}, { prop, val }) => {
    commit('set', {
        prop: prop,
        val: val
    })
};
