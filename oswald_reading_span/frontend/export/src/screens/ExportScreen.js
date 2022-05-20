import React from "react";
import autoBind from "auto-bind";
import RSPANResultTable from "../components/export_table";
import { SelectStyle } from "../components/datatable";

import "./ExportScreen.css";

export default class ExportScreen extends React.Component {
  constructor(props) {
    super(props);
    autoBind(this);
  }

  render() {
    return (
      <div className="export-screen">
        <RSPANResultTable
          tableId={"export-table"}
          selectStyle={SelectStyle.OS}
          ref={this.exportTableRef}
          initiateDataLoad={this.initiateDataLoad}
        />
      </div>
    );
  }

  async initiateDataLoad() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([]);
      }, 1000);
    });
  }
}
