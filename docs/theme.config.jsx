import YouTube from './components/YouTube'

const github = 'https://github.com/mateusztylec/gaidme';

export default {
    docsRepositoryBase: `${github}/blob/main/docs`,
    project: {
        link: github
    },
    logo: <strong>gaidme docs</strong>,
    useNextSeoProps() {
        return {
            titleTemplate: '%s - gaidme Documentation',
        };
    },
    components: {
        YouTube
    },
    // ... other theme options
}