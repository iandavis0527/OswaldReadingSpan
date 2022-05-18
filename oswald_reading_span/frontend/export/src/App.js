import "./App.css";
import { RSPANResultTable } from "./export_table";

function App() {
  return (
    <div className="App">
      <RSPANResultTable
        tableId={"export-table"}
        serverDriver={this.props.serverDriver}
        selectStyle={SelectStyle.OS}
        ref={this.exportTableRef}
      />
    </div>
  );
}

export default App;
