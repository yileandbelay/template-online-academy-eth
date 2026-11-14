import CatalogueFilter from '../../components/CatalogueFilter';
import { courses } from '../../lib/data';
export default function Catalogue() {
  return (<><h1>Browse courses</h1><CatalogueFilter courses={courses} /></>);
}
