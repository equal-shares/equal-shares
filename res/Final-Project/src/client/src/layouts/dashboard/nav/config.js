// component
import SvgColor from '../../../components/svg-color/SvgColor';

const icon = (name) => <SvgColor src={`/assets/icons/navbar/${name}.svg`} sx={{ width: 1, height: 1 }} />;

const navConfig = [

  {
    title: 'home',
    path: '/peoples_budget/home',
    icon: icon('ic_home'),
  },
  {
    title: 'voting',
    path: '/peoples_budget/voting',
    icon: icon('ic_voting'),
  },
  {
    title: 'information',
    path: '/peoples_budget/information',
    icon: icon('ic_info'),
  },
  {
    title: 'dashboard',
    path: '/peoples_budget/dashboard',
    icon: icon('ic_graph'),
  },
  {
    title: 'results',
    path: '/peoples_budget/results',
    icon: icon('ic_results'),
  },
  {
    title: 'about us',
    path: '/peoples_budget/about_us',
    icon: icon('ic_aboutUs'),
  },
];

export default navConfig;
