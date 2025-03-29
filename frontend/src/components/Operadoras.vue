<template>
  <div>
    <h1>Buscar Operadoras</h1>

    <!-- Container principal -->
    <div class="container">

      <!-- Quadro de Filtros -->
      <div class="filters-container">
        <h2 class="filters-title">Filtros</h2> <!-- Título do quadro -->
        <form @submit.prevent="buscarOperadoras">

          <!-- Primeira Row: Input Razão Social -->
          <div class="filters-row">
            <div class="filter-item">
              <label for="query" class="filter-label">Razão Social</label>
              <input type="text" id="query" v-model="query" placeholder="Digite a Razão Social da Operadora"
                class="styled-input" />
            </div>
          </div>

          <!-- Segunda Row: Filtros e Botão -->
          <div class="filters-row">
            <!-- Select para Coluna de Ordenação -->
            <div class="filter-item">
              <label for="order_by" class="filter-label">Ordenar por</label>
              <multiselect id="order_by" v-model="order_by" :options="orderOptions" placeholder="Selecione a Ordenação"
                :searchable="true" :close-on-select="true" :clear-on-select="false" label="label" track-by="value"
                aria-label="" :show-labels="false" class="styled-select"></multiselect>
            </div>

            <!-- Select para Direção da Ordenação -->
            <div class="filter-item">
              <label for="order_dir" class="filter-label">Tipo de Ordenação</label>
              <multiselect id="order_dir" v-model="order_dir" :options="orderDirDisplayOptions"
                placeholder="Tipo de Ordenação" :searchable="true" :close-on-select="true" :clear-on-select="false"
                aria-label="" :show-labels="false" class="styled-select"></multiselect>
            </div>



            <!-- Botão de Buscar -->
            <div class="button-container">
              <button type="submit" class="styled-button">Buscar</button>
            </div>
          </div>
        </form>
      </div>

      <!-- Resultados -->
      <div class="resultados">

        <!-- Tabela de Resultados -->
        <div v-if="operadoras.length > 0">
          <h2>Resultados Encontrados:</h2>
          <table class="table">
            <thead>
              <tr>
                <th>Registro ANS</th>
                <th>CNPJ</th>
                <th class="razao-social">Razão Social</th>
                <th>Modalidade</th>
                <th class="centro">Cidade</th>
                <th class="centro">UF</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="operadora in operadoras" :key="operadora.Registro_ANS">
                <td>{{ operadora.Registro_ANS }}</td>
                <td class="cnpj">{{ formatarCNPJ(operadora.CNPJ?.toString()) }}</td>
                <td class="razao-social">{{ operadora.Razao_Social }}</td>
                <td>{{ operadora.Modalidade }}</td>
                <td class="cidade">{{ operadora.Cidade }}</td>
                <td class="centro">{{ operadora.UF }}</td>

              </tr>
            </tbody>
          </table>
        </div>

        <!-- Mensagem de Nenhum Resultado -->
        <div v-else-if="searchTriggered">
          <p>Nenhuma operadora encontrada. Tente novamente com outros critérios.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from "../services/api";
import Multiselect from "vue-multiselect";
import "@/styles/Operadoras.css";
import "vue-multiselect/dist/vue-multiselect.min.css";
import { toast } from 'vue3-toastify';

export default {
  name: "ListaOperadoras",
  components: {
    Multiselect
  },
  data() {
    return {
      query: '',
      order_by: null, // pré-selecionado
      order_dir: null, // pré-selecionado
      operadoras: [],
      searchTriggered: false,
      // Opções disponíveis para ordenação por coluna
      orderOptions: [
        { label: 'Registro ANS', value: 'Registro_ANS' },
        { label: 'CNPJ', value: 'CNPJ' },
        { label: 'Razão Social', value: 'Razao_Social' },
        { label: 'Modalidade', value: 'Modalidade' },
        { label: 'Cidade', value: 'Cidade' },
        { label: 'UF', value: 'UF' },
      ],
      orderDirDisplayOptions: ["Ascendente", "Descendente"]
    };
  },
  methods: {
    formatarCNPJ(cnpj) {
      if (!cnpj) return "Não informado";

      cnpj = cnpj.toString();

      // Adiciona zeros à esquerda até que o CNPJ tenha 14 dígitos
      while (cnpj.length < 14) {
        cnpj = "0" + cnpj;
      }

      // Aplica a máscara no formato XX.XXX.XXX/XXXX-XX
      return cnpj.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, "$1.$2.$3/$4-$5");
    },
    async buscarOperadoras() {
      try {
        // Limpa os dados existentes antes da nova busca
        this.operadoras = [];

        // Inicializa as variáveis para os valores dos selects
        const orderByValue = this.order_by?.value || null;
        const orderDirValue = this.order_dir || null;

        // Validação de ordenação
        if ((orderByValue && !orderDirValue) || (!orderByValue && orderDirValue)) {
          toast.error('Para usar a ordenação, preencha ambos: "Ordenar Por" e "Tipo de Ordenação".');
          return;
        }

        this.searchTriggered = true; // Indica que a busca foi realizada

        // Monta o corpo da requisição
        const requestBody = {
          query: this.query || '',
          order_by: orderByValue,
          order_dir: orderDirValue,
        };

        // Faz a chamada POST para a API (o token CSRF será incluído automaticamente pelo apiClient)
        const response = await apiClient.post('/operadoras', requestBody);

        // Valida a resposta e atualiza os dados
        if (response.data && Array.isArray(response.data)) {
          this.operadoras = response.data;
        } else {
          console.error('Resposta inesperada do backend:', response.data);
          this.operadoras = [];
        }
      } catch (error) {
        console.error('Erro ao buscar operadoras:', error);
        toast.error('Erro ao buscar operadoras. Verifique os logs.');
      }
    }

  }
}
</script>