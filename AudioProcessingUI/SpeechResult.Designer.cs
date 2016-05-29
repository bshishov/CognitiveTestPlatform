namespace AudioProcessingUI
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.testResultsButton = new System.Windows.Forms.Button();
            this.analyzeDbButton = new System.Windows.Forms.Button();
            this.dbPath = new System.Windows.Forms.TextBox();
            this.resultsPath = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // testResultsButton
            // 
            this.testResultsButton.Location = new System.Drawing.Point(548, 154);
            this.testResultsButton.Name = "testResultsButton";
            this.testResultsButton.Size = new System.Drawing.Size(273, 86);
            this.testResultsButton.TabIndex = 0;
            this.testResultsButton.Text = "Анализировать результаты тестов";
            this.testResultsButton.UseVisualStyleBackColor = true;
            this.testResultsButton.Click += new System.EventHandler(this.TestResultsButton_Click);
            // 
            // analyzeDbButton
            // 
            this.analyzeDbButton.Location = new System.Drawing.Point(119, 154);
            this.analyzeDbButton.Name = "analyzeDbButton";
            this.analyzeDbButton.Size = new System.Drawing.Size(273, 86);
            this.analyzeDbButton.TabIndex = 1;
            this.analyzeDbButton.Text = "Анализировать данные из БД";
            this.analyzeDbButton.UseVisualStyleBackColor = true;
            // 
            // dbPath
            // 
            this.dbPath.Location = new System.Drawing.Point(119, 113);
            this.dbPath.Name = "dbPath";
            this.dbPath.Size = new System.Drawing.Size(273, 20);
            this.dbPath.TabIndex = 2;
            // 
            // resultsPath
            // 
            this.resultsPath.Location = new System.Drawing.Point(548, 113);
            this.resultsPath.Name = "resultsPath";
            this.resultsPath.Size = new System.Drawing.Size(273, 20);
            this.resultsPath.TabIndex = 3;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(116, 86);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(35, 13);
            this.label1.TabIndex = 4;
            this.label1.Text = "label1";
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1045, 680);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.resultsPath);
            this.Controls.Add(this.dbPath);
            this.Controls.Add(this.analyzeDbButton);
            this.Controls.Add(this.testResultsButton);
            this.Name = "MainForm";
            this.Text = "Анализатор речевых сигналов";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button testResultsButton;
        private System.Windows.Forms.Button analyzeDbButton;
        private System.Windows.Forms.TextBox dbPath;
        private System.Windows.Forms.TextBox resultsPath;
        private System.Windows.Forms.Label label1;
    }
}

