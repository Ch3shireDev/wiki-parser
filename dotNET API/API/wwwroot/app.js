Vue.createApp({
    data() {
        return {
            tags: [],
            elements: [],
            types: []
        };
    },
    created() {
        this.fetchElements();
    },
    methods: {
        changeState(x) {
            x.selected = !x.selected;
            this.fetchElements();
        },
        selectedTags() {
            return this.tags.filter(tag => tag.selected);
        },

        selectedTagsUrlNames() {
            return this.selectedTags().map(tag => tag.urlName);
        },

        selectedTagsUrlNamesString() {
            return this.selectedTagsUrlNames().join(',');
        },

        selectedTypes() {
            return this.types.filter(type => type.selected);
        },

        selectedTypesUrlNames() {
            return this.selectedTypes().map(type => type.urlName);
        },

        selectedTypesUrlNamesString() {
            return this.selectedTypesUrlNames().join(',');
        },

        getParamsStr() {
            return {
                selectedTags: this.selectedTagsUrlNamesString(),
                selectedTypes: this.selectedTypesUrlNamesString()
            };
        },
        getParams() {
            return {
                selectedTags: this.selectedTagsUrlNames(),
                selectedTypes: this.selectedTypesUrlNames()
            };
        },

        fetchElements() {
            let params = this.getParams();
            let paramsStr = this.getParamsStr();
            axios.get('/api/elements', {
                params: paramsStr
            },
            ).then(response => {
                this.elements = response.data.elements;

                this.types = response.data.types;

                this.types.forEach(type => {
                    type.selected = params.selectedTypes.includes(type.urlName);
                });

                this.tags = response.data.tags;

                this.tags.forEach(tag => {
                    tag.selected = params.selectedTags.includes(tag.urlName);
                });
            });

        }

    }
}).mount('#app');